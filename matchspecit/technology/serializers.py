from rest_framework import serializers

from matchspecit.technology.models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["name"]
