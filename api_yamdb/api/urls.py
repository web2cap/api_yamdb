from django.urls import include, path
from rest_framework import routers

from .views import AuthViewSet, TitleViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
