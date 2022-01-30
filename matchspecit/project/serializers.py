from rest_framework import serializers

from matchspecit.project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name"]
