# absolute path: /workspaces/paddle/paddle/games/models.py

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.utils.text import slugify


DEFAULT_GROUP_NAME = "club moraleja"


def get_default_group():
    group, _ = Group.objects.get_or_create(
        slug=slugify(DEFAULT_GROUP_NAME),
        defaults={"name": DEFAULT_GROUP_NAME},
    )
    return group


def get_default_group_id():
    return get_default_group().id


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_lower_group_name",
            )
        ]
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def update_player_rankings(*, group=None):
    """
    Recalculates persisted `ranking_position` using the canonical ranking policy.

    Canonical policy is shared with frontend ranking pages:
    - sort key: wins desc, rounded win rate (2dp) desc, matches asc, name asc
    - tie key: wins + rounded win rate + matches
    - position style: competition ranking ("1224")

    Players with zero matches are persisted as unranked (`ranking_position = 0`).
    """
    from frontend.services.ranking import canonical_ranking_sort_key, canonical_ranking_tie_key

    players_qs = Player.objects.all()
    matches_qs = Match.objects.all()
    if group is not None:
        players_qs = players_qs.filter(group=group)
        matches_qs = matches_qs.filter(group=group)

    players = list(players_qs)
    if not players:
        return

    matches_qs = matches_qs.select_related(
        "team1_player1", "team1_player2", "team2_player1", "team2_player2"
    )
    stats: dict[int, dict[str, int]] = {}

    for match in matches_qs:
        match_players = [
            match.team1_player1,
            match.team1_player2,
            match.team2_player1,
            match.team2_player2,
        ]
        for player in match_players:
            row = stats.setdefault(player.id, {"matches": 0, "wins": 0})
            row["matches"] += 1

        winners = [match.team1_player1, match.team1_player2] if match.winning_team == 1 else [
            match.team2_player1,
            match.team2_player2,
        ]
        for winner in winners:
            stats[winner.id]["wins"] += 1

    ranked_players: list[Player] = []
    unranked_players: list[Player] = []
    for player in players:
        row = stats.get(player.id)
        if not row or row["matches"] == 0:
            unranked_players.append(player)
            continue

        matches_played = row["matches"]
        wins = row["wins"]
        win_rate = (wins / matches_played) * 100 if matches_played else 0.0
        player._ranking_wins = wins
        player._ranking_matches = matches_played
        player._ranking_win_rate = win_rate
        ranked_players.append(player)

    ranked_players.sort(
        key=lambda player: canonical_ranking_sort_key(
            wins=player._ranking_wins,
            win_rate=player._ranking_win_rate,
            matches=player._ranking_matches,
            name=player.name,
        )
    )

    last_tie_key = None
    last_rank = 0
    for ordinal, player in enumerate(ranked_players, start=1):
        tie_key = canonical_ranking_tie_key(
            wins=player._ranking_wins,
            win_rate=player._ranking_win_rate,
            matches=player._ranking_matches,
        )
        if tie_key != last_tie_key:
            last_tie_key = tie_key
            last_rank = ordinal

        if player.ranking_position != last_rank:
            player.ranking_position = last_rank
            player.save(update_fields=["ranking_position"])

    for player in unranked_players:
        if player.ranking_position != 0:
            player.ranking_position = 0
            player.save(update_fields=["ranking_position"])


class Player(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="players", default=get_default_group_id)
    name = models.CharField(max_length=100)
    registered_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    matches = models.ManyToManyField('Match', related_name='players', blank=True)
    ranking_position = models.PositiveIntegerField(default=0)

    # --- Gender field options and definitions: ---    
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,   # TEMPORARY: allows existing players until admin fills it
        blank=True,  # TEMPORARY
    )

    class Meta:
        """
        Forces the database to store and check names case-insensitively.
        For instance: prevents the creation of players like "john" and "John" separately.
        """
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='unique_lower_name',
                violation_error_message="Player name must be globally unique (case insensitive)"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.group_id:
            self.group = get_default_group()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # ==== Calculated player stats ====
    @property
    def matches_played(self):
        return self.matches.count() if self.id else 0

    @property
    def wins(self):
        # Count matches where this player is in the winning team
        return Match.objects.filter(
            models.Q(team1_player1=self, winning_team=1) |
            models.Q(team1_player2=self, winning_team=1) |
            models.Q(team2_player1=self, winning_team=2) |
            models.Q(team2_player2=self, winning_team=2)
        ).count()

    @property
    def win_rate(self):
        if self.matches_played == 0:
            return 0.0
        return (self.wins / self.matches_played) * 100

    @property
    def losses(self):
        return max(0, self.matches_played - self.wins)

    # Data integrity is enforced in views/serializers to avoid partial updates
    # during cascading changes  (e.g., match deletions).



class Match(models.Model):
    APPROVAL_WINDOW_DAYS = 30

    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="matches", default=get_default_group_id)
    team1_player1 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='team1_player1_matches')
    team1_player2 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='team1_player2_matches')
    team2_player1 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='team2_player1_matches')
    team2_player2 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='team2_player2_matches')
    winning_team = models.IntegerField(choices=[(1, "Team 1"), (2, "Team 2")], null=False)
    date_played = models.DateField()
    
    # --- Match gender field options and definitions: ---
    GENDER_TYPE_UNKNOWN = "U"
    GENDER_TYPE_MALE = "M"
    GENDER_TYPE_FEMALE = "F"
    GENDER_TYPE_MIXED = "X"
    GENDER_TYPE_CHOICES = [
        (GENDER_TYPE_UNKNOWN, "Unknown"),
        (GENDER_TYPE_MALE, "Men"),
        (GENDER_TYPE_FEMALE, "Women"),
        (GENDER_TYPE_MIXED, "Mixed"),
    ]
    match_gender_type = models.CharField(
        max_length=1,
        choices=GENDER_TYPE_CHOICES,
        null=True,   # TEMPORARY
        blank=True,  # TEMPORARY
        db_index=True,  # important for ranking filters
    )

    def __str__(self):
        return f"Match on {self.date_played}"

    @classmethod
    def editable_date_floor(cls, today=None):
        from datetime import date, timedelta

        today = today or date.today()
        return today - timedelta(days=cls.APPROVAL_WINDOW_DAYS)

    def is_locked(self, today=None):
        return self.date_played < self.editable_date_floor(today=today)

    @property
    def all_players(self):
        return [
            self.team1_player1,
            self.team1_player2,
            self.team2_player1,
            self.team2_player2,
        ]

    @property
    def winning_players(self):
        if self.winning_team == 1:
            return [self.team1_player1, self.team1_player2]
        elif self.winning_team == 2:
            return [self.team2_player1, self.team2_player2]
        return []

    @property
    def losing_players(self):
        if self.winning_team == 1:
            return [self.team2_player1, self.team2_player2]
        elif self.winning_team == 2:
            return [self.team1_player1, self.team1_player2]
        return []
    
    def compute_gender_type(self) -> str:
        """
        Computes match gender type from the 4 players.
        Possibilities: Men (all players are M), Women (all players are F) and Mixed (contains both M and F).
        """
        genders = {p.gender for p in self.all_players if p and p.gender}
        if genders == {Player.GENDER_MALE}:
            return Match.GENDER_TYPE_MALE
        if genders == {Player.GENDER_FEMALE}:
            return Match.GENDER_TYPE_FEMALE
        # Any combination containing both genders is mixed
        return Match.GENDER_TYPE_MIXED

    def clean(self):
        player_groups = {player.group_id for player in self.all_players if player}
        if len(player_groups) > 1:
            raise ValidationError("Todos los jugadores del partido deben pertenecer al mismo grupo.")
        if player_groups:
            group_id = next(iter(player_groups))
            if self.group_id and self.group_id != group_id:
                raise ValidationError("El grupo del partido no coincide con el grupo de sus jugadores.")
            self.group_id = group_id

    def apply_match_effects(self):
        # Add this match to all players' matches
        for player in self.all_players:
            player.matches.add(self)
        update_player_rankings(group=self.group)

    def revert_match_effects(self):
        # Remove this match from all players' matches
        for player in self.all_players:
            player.matches.remove(self)
        update_player_rankings(group=self.group)

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        # If editing, revert old effects first (uses old FKs)
        if not is_new:
            old = Match.objects.get(pk=self.pk)
            old.revert_match_effects()

        if not self.group_id:
            self.group = self.team1_player1.group

        # Compute match gender type from the (new/current) players
        self.clean()
        self.match_gender_type = self.compute_gender_type()

        super().save(*args, **kwargs)

        # Apply effects using current FKs
        self.apply_match_effects()


    def delete(self, *args, **kwargs):
        self.revert_match_effects()
        super().delete(*args, **kwargs)

    def update_match(self, **kwargs):
        """
        Usage: match.update_match(team1_player1=..., team1_player2=..., ...)
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        # Let save() handle:
        # - revert old effects
        # - recompute match_gender_type
        # - apply new effects
        self.save()
