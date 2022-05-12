from django.urls import include, path
from rest_framework import routers

from .views import (
    AuthViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet
)

app_name = "api"

router = routers.DefaultRouter()
router.register("auth", AuthViewSet, basename="auth")
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")

urlpatterns = [
    path("v1/", include(router.urls)),
]
