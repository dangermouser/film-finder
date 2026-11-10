from rest_framework import viewsets
from .models import Film
from .serializers import FilmSerializer

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all().order_by("title")
    serializer_class = FilmSerializer