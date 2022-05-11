from django.urls import include, path
from rest_framework import routers

from .views import AuthViewSet, TitleViewSet, GenreViewSet, CategoryViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
