# paddle/games/management/commands/list_players_registration.py

from django.core.management.base import BaseCommand
from games.models import Player


class Command(BaseCommand):
    help = "List registered and unregistered players."

    def handle(self, *args, **options):
        registered = Player.objects.filter(registered_user__isnull=False).order_by("name")
        unregistered = Player.objects.filter(registered_user__isnull=True).order_by("name")

        self.stdout.write("=== Registered players ===")
        if registered.exists():
            for p in registered:
                self.stdout.write(f"- {p.name}")
        else:
            self.stdout.write("(none)")

        self.stdout.write("\n=== Unregistered players ===")
        if unregistered.exists():
            for p in unregistered:
                self.stdout.write(f"- {p.name}")
        else:
            self.stdout.write("(none)")
