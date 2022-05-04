from rest_framework import serializers

from matchspecit.technology.models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Technology
        fields = ("id", "name")
