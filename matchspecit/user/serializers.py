from django.contrib.auth import get_user_model
from rest_framework import serializers

from matchspecit.technology.models import Technology
from matchspecit.technology.serializers import TechnologySerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_login",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_joined",
            "description",
            "is_matchable",
            "technologies",
        )
