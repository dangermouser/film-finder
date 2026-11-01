from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=100, blank="True", default="")
    director = models.CharField(max_length=200, blank=True, default="")
    plot = models.TextField(blank=True, default="")
    imdb_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
