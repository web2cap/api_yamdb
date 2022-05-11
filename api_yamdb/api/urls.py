from django.urls import include, path
from rest_framework import routers

from .views import (
    AuthViewSet,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

app_name = "api"

router = routers.DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("users", UserViewSet, basename="users")
router.register(r'categories', CategoryViewSet, basename="Genre")
router.register(r'genres', GenreViewSet, basename="categories")
router.register(r'titles', TitleViewSet, basename="Title")

urlpatterns = [
    path("v1/", include(router.urls)),
]
