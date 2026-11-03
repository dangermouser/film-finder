import csv

from django.core.management.base import BaseCommand

from films.models import Film
from films.omdb_client import get_film, OmdbError

class Command(BaseCommand):
    help = "Import films from a CSV file, enriching them via OMDb"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")

    def handle(self, *args, **options):
        self.stdout.write(f"Reading {options['csv_path']}")

        with open(options["csv_path"], newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row["title"].strip()
                year = row["year"].strip()

                try:
                    data = get_film(title, year)
                except OmdbError as e:
                    self.stdout.write(self.style.WARNING(f"Skipped {title} ({year}): {e}"))
                    continue

                self.stdout.write(f"Found {data['Title']} ({data['imdbID']})")