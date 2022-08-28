from django.contrib.auth import get_user_model
from rest_framework import serializers

from matchspecit.project.models import Project

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        allow_null=True,
        default=None,
    )
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=False)

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
            "image",
        ]

    def validate_owner(self, value):
        return self.context["request"].user
