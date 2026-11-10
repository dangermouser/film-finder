from datetime import date
from rest_framework import serializers
from .models import Film
import re

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ["id", "title", "year", "genre", "director", "plot", "imdb_id"]

    def validate_year(self, value):
        max_year = date.today().year + 5
        if value < 1888 or value > max_year:
            raise serializers.ValidationError(
                f"Year must be between 1888 and {max_year}."
            )
        return value

    def validate_imdb_id(self, value):
        if not re.fullmatch(r"tt\d+", value):
            raise serializers.ValidationError(
                "IMDb ID must look like 'tt' followed by digits, e.g. tt0113277."
            )
        return value
    
    