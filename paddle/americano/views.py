# americano/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.views.decorators.http import require_POST
from django.db.models.functions import Lower
from django.db.models import F

from .forms import AmericanoTournamentForm
from .models import AmericanoTournament, AmericanoRound, AmericanoMatch, AmericanoPlayerStats
from games.models import Player
from frontend.view_modules.common import get_request_group_context, get_user_group, get_user_player

def americano_create_next_round(tournament: AmericanoTournament) -> AmericanoRound:
    """
    Creates the next round (number = count+1) and the empty matches (players/4).
    Players/court/scores remain NULL.
    """
    round_number = tournament.rounds.count() + 1
    new_round = AmericanoRound.objects.create(tournament=tournament, number=round_number)

    matches_count = tournament.players.count() // 4
    for _ in range(matches_count):
        AmericanoMatch.objects.create(round=new_round)

    return new_round

def americano_can_edit(request, tournament: AmericanoTournament) -> bool:
    """
    Edit capabilities if:
    - authenticated and tournament open for edit (until tournament day inclusive); and
    - user is either:
        - a tournament participant (linked Player), OR
        - the tournament creator, OR
        - staff
    """
    if not request.user.is_authenticated:
        return False

    if not tournament.is_open_for_edit:
        return False

    if request.user.is_staff:
        return True

    if tournament.created_by_id == request.user.id:
        return True

    return tournament.players.filter(registered_user=request.user).exists()

def recompute_americano_standings(tournament: AmericanoTournament) -> None:
    """
    Recompute tournament standings from scratch based on current saved and complete matches.
    Robust to edits: no double counting (idempotent standings).
    Rules:
    - Each player in winning team: +1 win, 
    - Each player in losing team: +1 loss, 
    - Every player in a completed match: +1 played,
    - points_for/against accumulated from team points, and
    - ignore computing matches with missing players or scores.
    """
    # Ensure stats rows exist: every tournament player has a stats object.
    for p in tournament.players.all():
        AmericanoPlayerStats.objects.get_or_create(tournament=tournament, player=p)

    # Reset stats: this is the key to idempotency; 
    # previous runs or edits do not matter because the function always starts from zero.
    AmericanoPlayerStats.objects.filter(tournament=tournament).update(
        wins=0,
        losses=0,
        matches_played=0,
        points_for=0,
        points_against=0,        
    )

    # Loads all stats rows for the tournament into Python and indexes them by player_id.
    stats = {
        s.player_id: s
        for s in AmericanoPlayerStats.objects.filter(tournament=tournament)
    }

    # Filters matches to those whose round belongs to the given tournament,
    # and preloads the four player foreign keys in the same query.
    matches = (
        AmericanoMatch.objects
        .filter(round__tournament=tournament)
        .select_related("team1_player1", "team1_player2", "team2_player1", "team2_player2")
    )

    # Iterate over all matches, skip incomplete ones and update stats
    for m in matches:
        # skip matches where any of the four players is missing
        if not all([m.team1_player1_id, m.team1_player2_id, m.team2_player1_id, m.team2_player2_id]):
            continue
        # skip matches where one or both scores are None
        if m.team1_points is None or m.team2_points is None:
            continue
        
        # Extract scores (numeric) and teams (list of player ids)
        s1 = int(m.team1_points)
        s2 = int(m.team2_points)
        t1 = [m.team1_player1_id, m.team1_player2_id]
        t2 = [m.team2_player1_id, m.team2_player2_id]
        
        # Accumulate played matches for all 4 players
        for pid in (t1 + t2):
            st = stats.get(pid)
            if st:
                st.matches_played += 1
        
        # Accumulate points for/against
        for pid in t1:
            st = stats.get(pid)
            if st:
                st.points_for += s1
                st.points_against += s2

        for pid in t2:
            st = stats.get(pid)
            if st:
                st.points_for += s2
                st.points_against += s1

        # Accumulate wins/losses; if tie (s1 == s2): no wins/losses added
        if s1 > s2:
            # Team 1 wins, Team 2 loses
            for pid in t1:
                st = stats.get(pid)
                if st:
                    st.wins += 1
            for pid in t2:
                st = stats.get(pid)
                if st:
                    st.losses += 1

        elif s2 > s1:
            # Team 2 wins, Team 1 loses
            for pid in t2:
                st = stats.get(pid)
                if st:
                    st.wins += 1
            for pid in t1:
                st = stats.get(pid)
                if st:
                    st.losses += 1
        

    # Writes all in‑memory changes back to the database in a single bulk operation,
    # is more efficient for many players than repeated .save() calls inside the loop.
    AmericanoPlayerStats.objects.bulk_update(
        stats.values(),
        ["wins", "losses", "matches_played", "points_for", "points_against"],
    )


def _parse_americano_round_assignment(round_obj: AmericanoRound, post_data):
    tournament = round_obj.tournament
    allowed_player_ids = set(tournament.players.values_list("id", flat=True))
    players_by_id = {p.id: p for p in tournament.players.all()}
    matches = list(round_obj.matches.all())
    used_in_fully_assigned = set()
    updates = []

    def parse_pid(raw):
        raw = (raw or "").strip()
        if not raw:
            return None
        try:
            pid = int(raw)
        except ValueError:
            return None
        return pid

    def parse_score(value):
        value = (value or "").strip()
        if value == "":
            return None
        try:
            parsed = int(value)
        except ValueError:
            return None
        return parsed if parsed >= 0 else None

    def parse_court(value, current_value):
        value = (value or "").strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            return current_value

    for match in matches:
        pids = {
            "t1p1": parse_pid(post_data.get(f"match_{match.id}_t1p1")),
            "t1p2": parse_pid(post_data.get(f"match_{match.id}_t1p2")),
            "t2p1": parse_pid(post_data.get(f"match_{match.id}_t2p1")),
            "t2p2": parse_pid(post_data.get(f"match_{match.id}_t2p2")),
        }

        for pid in pids.values():
            if pid is not None and pid not in allowed_player_ids:
                return None, "Selección inválida: hay jugadores fuera del torneo."

        fully_assigned = all(pid is not None for pid in pids.values())
        if fully_assigned:
            pid_list = list(pids.values())
            if len(set(pid_list)) != 4:
                return None, "Un jugador no puede repetirse dentro del mismo partido."
            if any(pid in used_in_fully_assigned for pid in pid_list):
                return None, "Un jugador no puede repetirse en la misma ronda."
            used_in_fully_assigned.update(pid_list)

        s1 = parse_score(post_data.get(f"match_{match.id}_score1"))
        s2 = parse_score(post_data.get(f"match_{match.id}_score2"))
        if not fully_assigned or (s1 is None and s2 is None):
            s1 = None
            s2 = None

        updates.append(
            {
                "match": match,
                "team1_player1": players_by_id.get(pids["t1p1"]),
                "team1_player2": players_by_id.get(pids["t1p2"]),
                "team2_player1": players_by_id.get(pids["t2p1"]),
                "team2_player2": players_by_id.get(pids["t2p2"]),
                "court_number": parse_court(
                    post_data.get(f"match_{match.id}_court"),
                    match.court_number,
                ),
                "team1_points": s1,
                "team2_points": s2,
            }
        )

    return updates, None


def _save_americano_round_assignment(tournament: AmericanoTournament, updates, *, create_next_round=False):
    with transaction.atomic():
        for update in updates:
            match = update["match"]
            match.team1_player1 = update["team1_player1"]
            match.team1_player2 = update["team1_player2"]
            match.team2_player1 = update["team2_player1"]
            match.team2_player2 = update["team2_player2"]
            match.court_number = update["court_number"]
            match.team1_points = update["team1_points"]
            match.team2_points = update["team2_points"]
            match.save()

        recompute_americano_standings(tournament)

        if create_next_round:
            americano_create_next_round(tournament)


@login_required
def americano_new(request):
    user_group = get_user_group(request)
    if request.method == "POST":
        form = AmericanoTournamentForm(request.POST, group=user_group)

        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.group = user_group
            tournament.save()

            # Combine selected players + newly created players
            selected_players = list(form.cleaned_data["players"])
            new_entries = form.cleaned_data.get("new_player_entries", [])

            created_players = []
            for name, gender in new_entries:
                normalized = name.strip()
                if not normalized:
                    continue

                # Respect case-insensitive uniqueness constraint
                player = Player.objects.filter(name__iexact=normalized, group=user_group).first()
                if player is None:
                    try:
                        player = Player.objects.create(name=normalized, gender=gender, group=user_group)
                    except IntegrityError:
                        # Safety net for race conditions / DB constraint hit
                        player = Player.objects.filter(name__iexact=normalized, group=user_group).first()
                elif not player.gender:
                    player.gender = gender
                    player.save(update_fields=["gender"])

                if player:
                    created_players.append(player)

            all_players = selected_players + created_players
            tournament.players.set(all_players)

            # Initialize stats for all players
            for p in tournament.players.all():
                AmericanoPlayerStats.objects.get_or_create(
                    tournament=tournament,
                    player=p,
                )

            return redirect("americano_detail", pk=tournament.pk)

    else:
        form = AmericanoTournamentForm(group=user_group)

        # Preselect creator player (GET only)
        player = get_user_player(request)
        if player:
            form.fields["players"].initial = [player.pk]

    return render(
        request,
        "frontend/americano/americano_new.html",
        {"form": form},
    )

def americano_list(request):
    today = timezone.localdate()
    group_context = get_request_group_context(request)
    queryset = AmericanoTournament.objects.all()
    if group_context["group"] is not None:
        queryset = queryset.filter(group=group_context["group"])

    ongoing = (
        queryset
        .filter(is_active=True, play_date__gte=today)
        .order_by("play_date", "name")
    )

    finished = (
        queryset
        .filter(play_date__lt=today)
        .order_by("-play_date", "name")
    )

    return render(
        request,
        "frontend/americano/americano_list.html",
        {"ongoing": ongoing, "finished": finished, "group_display_name": group_context["display_name"]},
    )


def americano_detail(request, pk):
    group_context = get_request_group_context(request)
    queryset = AmericanoTournament.objects.all()
    if group_context["group"] is not None:
        queryset = queryset.filter(group=group_context["group"])
    tournament = get_object_or_404(queryset, pk=pk)

    # Edit capabilities: participants/staff/creator and only until tournament day (inclusive)
    can_edit = americano_can_edit(request, tournament)

    americano_players = list(tournament.players.order_by(Lower("name")))
    match_queryset = AmericanoMatch.objects.select_related(
        "team1_player1",
        "team1_player2",
        "team2_player1",
        "team2_player2",
    )
    rounds = tournament.rounds.prefetch_related(Prefetch("matches", queryset=match_queryset))
    
    for r in rounds:
        r.sorted_matches = sorted(
            r.matches.all(),
            key=lambda m: (m.court_number is None, m.court_number or 0, m.id),
        )
    
    standings = (
        AmericanoPlayerStats.objects
        .filter(tournament=tournament)
        .select_related("player")
        .annotate(points_diff=F("points_for") - F("points_against"))
        .order_by("-wins", "-points_diff", "-points_for", Lower("player__name"))
    )
    
    # Compute competition ranking positions with ties:
    # Players with exactly the same metrics share the same position
    # Example: Competition ranking (“1224” style), not ordinal ranking (“1234”)
    # Display the rank number only on the first row of the tie group
    ranked_standings = []

    last_key = None
    last_position = None

    for index, row in enumerate(standings, start=1):
        key = (row.wins, row.points_diff, row.points_for)

        if key != last_key:
            # New rank group
            row.display_position = index
            row.show_position = True
            last_position = index
            last_key = key
        else:
            # Same rank as previous
            row.display_position = last_position
            row.show_position = False

        ranked_standings.append(row)

    return render(
        request,
        "frontend/americano/americano_detail.html",
        {
            "tournament": tournament,
            "rounds": rounds,
            "americano_players": americano_players,
            "standings": ranked_standings,
            "can_edit": can_edit,
            "group_display_name": group_context["display_name"],
        },
    )

@login_required
@require_POST
def americano_new_round(request, pk):
    tournament = get_object_or_404(AmericanoTournament, pk=pk)

    # Edit capabilities: participants/staff/creator and only until tournament day (inclusive)
    can_edit = americano_can_edit(request, tournament)
    
    if not can_edit:
        return redirect("americano_detail", pk=tournament.pk)

    # Create next round
    americano_create_next_round(tournament)

    return redirect("americano_detail", pk=tournament.pk)

@require_POST
@login_required
def americano_assign_round(request, round_id):
    round_obj = get_object_or_404(AmericanoRound, pk=round_id)    
    tournament = round_obj.tournament

    # Edit capabilities: participants/staff/creator and only until tournament day (inclusive)
    can_edit = americano_can_edit(request, tournament)
    
    if not can_edit:
        return redirect("americano_detail", pk=tournament.pk)

    updates, error = _parse_americano_round_assignment(round_obj, request.POST)
    if error:
        request.session["americano_round_error"] = error
        return redirect("americano_detail", pk=tournament.pk)

    request.session.pop("americano_round_error", None)
    _save_americano_round_assignment(
        tournament,
        updates,
        create_next_round=request.POST.get("action") == "new_round",
    )

    return redirect("americano_detail", pk=tournament.pk)

@require_POST
@login_required
def americano_delete_round(request, round_id):
    round_obj = get_object_or_404(AmericanoRound, pk=round_id)
    tournament = round_obj.tournament

    # Edit capabilities: participants/staff/creator and only until tournament day (inclusive)
    can_edit = americano_can_edit(request, tournament)
    
    if not can_edit:
        return redirect("americano_detail", pk=tournament.pk)

    round_obj.delete()

    # Renumber remaining rounds to keep 1..N
    remaining = tournament.rounds.order_by("number")
    for i, r in enumerate(remaining, start=1):
        if r.number != i:
            r.number = i
            r.save(update_fields=["number"])

    recompute_americano_standings(tournament)
    
    request.session.pop("americano_round_error", None)
    return redirect("americano_detail", pk=tournament.pk)

@require_POST
@login_required
def americano_delete_tournament(request, pk):
    tournament = get_object_or_404(AmericanoTournament, pk=pk)

    can_delete = request.user.is_staff or (tournament.created_by_id == request.user.id)
    if not can_delete:
        return redirect("americano_detail", pk=tournament.pk)

    tournament.delete()
    return redirect("americano_list")
