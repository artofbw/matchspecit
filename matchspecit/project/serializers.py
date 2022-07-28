from rest_framework import serializers
from matchspecit.project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description", "created_at", "updated_at", "owner", "is_matchable", "is_finish", "is_successful", "technologies", "image"]
