from django.contrib.auth import get_user_model
from rest_framework import serializers

from matchspecit.match.models import Match
from matchspecit.project.serializers import ProjectSerializer
from matchspecit.user.serializers import UserSerializer

User = get_user_model()


class MatchSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Match
        depth = 1
        fields = [
            "id",
            "user",
            "project",
            "match_percent",
            "project_owner_approved",
            "specialist_approved",
        ]


class MatchSpecialistSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Match
        depth = 1
        fields = [
            "id",
            "project",
            "match_percent",
            "project_owner_approved",
            "specialist_approved",
        ]


class MatchProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Match
        depth = 1
        fields = [
            "id",
            "user",
            "match_percent",
            "project_owner_approved",
            "specialist_approved",
        ]


class MatchPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            "project_owner_approved",
            "specialist_approved",
        ]
