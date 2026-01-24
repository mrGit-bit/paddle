# absolute path: /workspaces/paddle/paddle/games/models.py

from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User

def update_player_rankings():
    """
    Recalculates the ranking position of all players in the database.
    Ranking is done by wins, then by win rate (only if the player has played a match),
    and finally by name (case insensitive).
    """
    players = list(Player.objects.all())
    players.sort(
        key=lambda p: (-p.wins, -p.win_rate if p.matches_played > 0 else 0, p.name.lower())
    )
    for idx, player in enumerate(players, start=1):
        if player.ranking_position != idx:
            player.ranking_position = idx
            player.save(update_fields=['ranking_position'])
            

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
                violation_error_message="Player name must be unique (case insensitive)"
            )
        ]

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

    def apply_match_effects(self):
        # Add this match to all players' matches
        for player in self.all_players:
            player.matches.add(self)
        update_player_rankings()

    def revert_match_effects(self):
        # Remove this match from all players' matches
        for player in self.all_players:
            player.matches.remove(self)
        update_player_rankings()

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        # If editing, revert old effects first (uses old FKs)
        if not is_new:
            old = Match.objects.get(pk=self.pk)
            old.revert_match_effects()

        # Compute match gender type from the (new/current) players
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




