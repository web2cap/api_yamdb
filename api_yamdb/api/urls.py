from django.urls import include, path
from rest_framework import routers

from .views import AuthViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")

urlpatterns = [
    path("v1/", include(router.urls)),
]
