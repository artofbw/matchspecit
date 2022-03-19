from django.contrib import admin
from django.contrib.admin import ModelAdmin

from matchspecit.technology.models import Technology


class TechnologyAdmin(ModelAdmin):
    model = Technology
    list_display = ("name",)
    fieldsets = ((None, {"fields": ("name",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name",),
            },
        ),
    )
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Technology, TechnologyAdmin)
