# americano/context_processors.py
from django.utils import timezone

from .models import AmericanoTournament


def americano_nav(request):
    today = timezone.localdate()

    ongoing = (
        AmericanoTournament.objects
        .filter(is_active=True, play_date__gte=today)
        .order_by("play_date", "name")
    )

    finished = (
        AmericanoTournament.objects
        .filter(play_date__lt=today)
        .order_by("-play_date", "name")[:10]
    )

    return {
        "americano_ongoing_tournaments": ongoing,
        "americano_finished_tournaments": finished,
    }
