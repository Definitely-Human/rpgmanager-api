from django.contrib import admin
from djangoapps.rpg import models
from django.utils.translation import gettext_lazy as _


class CharacterAdmin(admin.ModelAdmin):
    ordering = ["-id"]
    list_display = ["id", "name", "user", "character_xp", "coins"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "user"]
    fieldsets = (
        (
            None,
            {
                "fields": ("user",),
            },
        ),
        (
            _("Info"),
            {
                "fields": ("name",),
            },
        ),
        (
            _("Data"),
            {
                "fields": ("coins", "character_xp"),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at",),
            },
        ),
    )
    readonly_fields = [
        "created_at",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": ("user",),
            },
        ),
        (
            _("Info"),
            {
                "fields": ("name",),
            },
        ),
        (
            _("Data"),
            {
                "fields": ("coins", "character_xp"),
            },
        ),
    )


admin.site.register(models.Character, CharacterAdmin)
