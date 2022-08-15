from django.contrib import admin
from django.contrib.admin import ModelAdmin

from matchspecit.match.models import Match


class MatchAdmin(ModelAdmin):
    model = Match
    list_display = (
        "user",
        "project",
        "match_percent",
        "created_at",
    )
    fieldsets = ((None, {"fields": ("user", "project", "match_percent", "created_at")}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("user", "project", "match_percent", "created_at"),
            },
        ),
    )


admin.site.register(Match, MatchAdmin)
