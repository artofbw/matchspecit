from django.contrib import admin

from matchspecit.project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
