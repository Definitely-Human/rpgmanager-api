from django.contrib import admin
from djangoapps.manager import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class TaskAdmin(admin.ModelAdmin):
    """Define the admin page for the tasks."""

    ordering = ["-updated_at"]
    list_display = (
        "id",
        "title",
        "character",
        "category",
        "created_at",
        "due_to",
        "is_complete",
        "is_favorite",
        "is_deleted",
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = (
        "title",
        "content",
        "character",
    )
    list_editable = (
        "is_complete",
        "is_favorite",
        "is_deleted",
    )
    list_filter = (
        "is_complete",
        "category",
        "is_favorite",
        "is_deleted",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("character",),
            },
        ),
        (
            _("Data"),
            {
                "fields": (
                    "title",
                    "content",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "due_to",
                    "completion_time",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            _("Filtering"),
            {
                "fields": (
                    "is_complete",
                    "is_favorite",
                    "is_deleted",
                    "tags",
                    "category",
                )
            },
        ),
    )

    readonly_fields = [
        "created_at",
        "updated_at",
        "completion_time",
    ]

    add_fieldsets = (
        (
            None,
            {
                "fields": ("character",),
            },
        ),
        (
            _("Data"),
            {
                "fields": (
                    "title",
                    "content",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("due_to",),
            },
        ),
        (
            _("Filtering"),
            {
                "fields": (
                    "is_favorite",
                    "tags",
                    "category",
                )
            },
        ),
    )


class TagAdmin(admin.ModelAdmin):
    ordering = ["-id"]
    list_display = ["id", "name", "user"]
    list_display_links = ["id", "name"]
    search_fields = ("name", "user")


class CategoryAdmin(admin.ModelAdmin):
    ordering = ["-id"]
    list_display = ["id", "name", "user"]
    list_display_links = ["id", "name"]
    search_fields = ("name", "user")


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Category, CategoryAdmin)
