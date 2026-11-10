from rest_framework.routers import DefaultRouter
from .views import FilmViewSet

router = DefaultRouter()
router.register("films", FilmViewSet)

urlpatterns = router.urls

