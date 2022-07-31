from rest_framework import serializers
from matchspecit.project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "owner",
            "is_matchable",
            "is_finish",
            "is_successful",
            "is_deleted",
            "technologies",
            "image"]
