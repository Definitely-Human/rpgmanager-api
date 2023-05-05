"""
URL mappings for the RPG app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from djangoapps.rpg import views


router = DefaultRouter()
router.register("character", views.CharacterViewSet)

app_name = "rpg"

urlpatterns = [
    path("", include(router.urls)),
]
