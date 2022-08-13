from django.contrib.auth import get_user_model
from rest_framework import serializers

from matchspecit.project.models import Project

User = get_user_model()


class MatchSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        allow_null=True,
        default=None,
    )
    match_percent = serializers.FloatField(min_value=0, max_value=1)

    class Meta:
        model = Project
        depth = 1
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
            "image",
            "match_percent",
        ]
