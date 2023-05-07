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
router.register("tasks", views.TaskViewSet)
router.register("tags", views.TagViewSet)
router.register("categories", views.CategoryViewSet)

app_name = "manager"

urlpatterns = [
    path("", include(router.urls)),
]
