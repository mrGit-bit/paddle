# americano/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.db.models.functions import Lower
from django.db.models import F

from .forms import AmericanoTournamentForm
from .models import AmericanoTournament, AmericanoRound, AmericanoMatch, AmericanoPlayerStats
from games.models import Player

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

@login_required
def americano_new(request):
    if request.method == "POST":
        form = AmericanoTournamentForm(request.POST)

        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.save()

            # Combine selected players + newly created players
            selected_players = list(form.cleaned_data["players"])
            new_names = form.cleaned_data.get("new_player_names", [])

            created_players = []
            for name in new_names:
                normalized = name.strip()
                if not normalized:
                    continue

                # Respect case-insensitive uniqueness constraint
                player = Player.objects.filter(name__iexact=normalized).first()
                if player is None:
                    try:
                        player = Player.objects.create(name=normalized)
                    except IntegrityError:
                        # Safety net for race conditions / DB constraint hit
                        player = Player.objects.filter(name__iexact=normalized).first()

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
        form = AmericanoTournamentForm()

        # Preselect creator player (GET only)
        player = Player.objects.filter(registered_user=request.user).first()
        if player:
            form.fields["players"].initial = [player.pk]

    return render(
        request,
        "frontend/americano/americano_new.html",
        {"form": form},
    )

def americano_list(request):
    today = timezone.localdate()

    ongoing = (
        AmericanoTournament.objects
        .filter(is_active=True, play_date__gte=today)
        .order_by("play_date", "name")
    )

    finished = (
        AmericanoTournament.objects
        .filter(play_date__lt=today)
        .order_by("-play_date", "name")
    )

    return render(
        request,
        "frontend/americano/americano_list.html",
        {"ongoing": ongoing, "finished": finished},
    )


def americano_detail(request, pk):
    tournament = get_object_or_404(AmericanoTournament, pk=pk)

    # Edit capabilities: participants/staff/creator and only until tournament day (inclusive)
    can_edit = americano_can_edit(request, tournament)

    # rounds are ordered by number via Meta.ordering
    rounds = tournament.rounds.prefetch_related("matches")
    
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
            "standings": ranked_standings,
            "can_edit": can_edit,
        },
    )

@login_required
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

    allowed_player_ids = set(tournament.players.values_list("id", flat=True))

    matches = round_obj.matches.all()
    players_by_id = {p.id: p for p in tournament.players.all()}

    def parse_pid(raw):
        raw = (raw or "").strip()
        if not raw:
            return None
        try:
            pid = int(raw)
        except ValueError:
            return None
        return pid

    # We only enforce "no duplicates" across matches that are fully assigned (4 players)
    used_in_fully_assigned = set()

    def parse_score(v):
        v = (v or "").strip()
        if v == "":
            return None
        try:
            n = int(v)
        except ValueError:
            return None
        return n if n >= 0 else None

    for m in matches:
        # --- Players (can be partially filled) ---
        pids = {
            "t1p1": parse_pid(request.POST.get(f"match_{m.id}_t1p1")),
            "t1p2": parse_pid(request.POST.get(f"match_{m.id}_t1p2")),
            "t2p1": parse_pid(request.POST.get(f"match_{m.id}_t2p1")),
            "t2p2": parse_pid(request.POST.get(f"match_{m.id}_t2p2")),
        }

        # Validate player IDs (only if provided)
        for pid in pids.values():
            if pid is not None and pid not in allowed_player_ids:
                request.session["americano_round_error"] = "Selección inválida: hay jugadores fuera del torneo."
                return redirect("americano_detail", pk=tournament.pk)

        # Determine if the match has all 4 players selected
        fully_assigned = all(pid is not None for pid in pids.values())

        # If fully assigned, enforce no duplicates within this match and across other fully assigned matches
        if fully_assigned:
            pid_list = list(pids.values())

            # No duplicates inside the match
            if len(set(pid_list)) != 4:
                request.session["americano_round_error"] = "Un jugador no puede repetirse dentro del mismo partido."
                return redirect("americano_detail", pk=tournament.pk)

            # No duplicates across fully assigned matches in the round
            if any(pid in used_in_fully_assigned for pid in pid_list):
                request.session["americano_round_error"] = "Un jugador no puede repetirse en la misma ronda."
                return redirect("americano_detail", pk=tournament.pk)

            used_in_fully_assigned.update(pid_list)

            # Save players to DB
            m.team1_player1 = players_by_id[pids["t1p1"]]
            m.team1_player2 = players_by_id[pids["t1p2"]]
            m.team2_player1 = players_by_id[pids["t2p1"]]
            m.team2_player2 = players_by_id[pids["t2p2"]]
        else:
            # Allow partial save: keep whatever is selected, blank others
            m.team1_player1 = players_by_id.get(pids["t1p1"]) if pids["t1p1"] else None
            m.team1_player2 = players_by_id.get(pids["t1p2"]) if pids["t1p2"] else None
            m.team2_player1 = players_by_id.get(pids["t2p1"]) if pids["t2p1"] else None
            m.team2_player2 = players_by_id.get(pids["t2p2"]) if pids["t2p2"] else None

        # --- Court (always allowed, can be empty) ---
        court_val = request.POST.get(f"match_{m.id}_court", "").strip()

        if court_val == "":
            # Allow saving (or clearing) a null court number
            m.court_number = None
        else:
            try:
                m.court_number = int(court_val)
            except ValueError:
                # Ignore invalid input and keep the current value
                pass

        # --- Scores (only persist if match is fully assigned) ---
        s1 = parse_score(request.POST.get(f"match_{m.id}_score1"))
        s2 = parse_score(request.POST.get(f"match_{m.id}_score2"))

        if fully_assigned and (s1 is not None or s2 is not None):
            m.team1_points = s1
            m.team2_points = s2
        else:
            # If match isn't fully assigned, do not keep scores
            m.team1_points = None
            m.team2_points = None

        m.save()

    recompute_americano_standings(tournament)

    request.session.pop("americano_round_error", None)
    
    # If user clicked "Nueva ronda": save current round (already done) and create next one
    if request.POST.get("action") == "new_round":
        americano_create_next_round(tournament)

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
