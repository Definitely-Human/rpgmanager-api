"""
URL mappings for the manager app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from djangoapps.manager import views


router = DefaultRouter()
router.register("task", views.TaskViewSet)

app_name = "manager"

urlpatterns = [
    path("", include(router.urls)),
]
