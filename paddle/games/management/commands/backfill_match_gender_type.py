from django.core.management.base import BaseCommand
from django.db import transaction

from games.models import Match


class Command(BaseCommand):
    help = "Backfill match_gender_type for existing matches (where NULL/blank)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Bulk update batch size (default: 500).",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        qs = (
            Match.objects.filter(match_gender_type__isnull=True)
            .select_related("team1_player1", "team1_player2", "team2_player1", "team2_player2")
            .order_by("id")
        )

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No matches to backfill."))
            return

        self.stdout.write(f"Backfilling match_gender_type for {total} matches...")

        updated = 0
        buffer = []

        with transaction.atomic():
            for m in qs.iterator(chunk_size=batch_size):
                m.match_gender_type = m.compute_gender_type()
                buffer.append(m)

                if len(buffer) >= batch_size:
                    Match.objects.bulk_update(buffer, ["match_gender_type"])
                    updated += len(buffer)
                    buffer.clear()
                    self.stdout.write(f"  updated {updated}/{total}")

            if buffer:
                Match.objects.bulk_update(buffer, ["match_gender_type"])
                updated += len(buffer)
                self.stdout.write(f"  updated {updated}/{total}")

        self.stdout.write(self.style.SUCCESS(f"Done. Updated {updated} matches."))
