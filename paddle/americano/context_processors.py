# absolute path: /workspaces/paddle/paddle/americano/context_processors.py
from django.utils import timezone

from .models import AmericanoTournament
from frontend.view_modules.common import get_user_group


def americano_nav(request):
    today = timezone.localdate()
    user_group = get_user_group(request)
    queryset = AmericanoTournament.objects.all()
    if user_group is not None:
        queryset = queryset.filter(group=user_group)

    ongoing = (
        queryset
        .filter(is_active=True, play_date__gte=today)
        .order_by("play_date", "name")
    )

    finished = (
        queryset
        .filter(play_date__lt=today)
        .order_by("-play_date", "name")[:10]
    )

    return {
        "americano_ongoing_tournaments": ongoing,
        "americano_finished_tournaments": finished,
    }
