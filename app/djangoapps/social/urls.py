"""
URL mappings for the social app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from djangoapps.social import views


router = DefaultRouter()
router.register("profile", views.ProfileViewSet)

app_name = "social"

urlpatterns = [
    path("", include(router.urls)),
]
