import csv

from django.core.management.base import BaseCommand

from films.models import Film
from films.omdb_client import get_film, OmdbError


def clean(value):
    """OMDb sends 'N/A' for missing values; store an empty string instead."""
    return "" if value == "N/A" else value


class Command(BaseCommand):
    help = "Import films from a CSV file, enriching them via OMDb"

    def add_arguments(self, parser):
        parser.add_argument("csv_path")

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        failed_count = 0

        with open(options["csv_path"], newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row["title"].strip()
                year = row["year"].strip()

                try:
                    data = get_film(title, year)
                    film_year = int(data["Year"])
                except OmdbError as e:
                    self.stdout.write(self.style.WARNING(f"Skipped {title} ({year}): {e}"))
                    failed_count += 1
                    continue
                except ValueError:
                    self.stdout.write(self.style.WARNING(
                        f"Skipped {title} ({year}): unsupported year format {data['Year']}"
                    ))
                    failed_count += 1
                    continue

                film, created = Film.objects.update_or_create(
                    imdb_id=data["imdbID"],
                    defaults={
                        "title": data["Title"],
                        "year": film_year,
                        "genre": clean(data.get("Genre", "")),
                        "director": clean(data.get("Director", "")),
                        "plot": clean(data.get("Plot", "")),
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done: {created_count} created, {updated_count} updated, {failed_count} failed"
        ))