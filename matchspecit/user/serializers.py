from django.contrib.auth import get_user_model
from rest_framework import serializers

from matchspecit.technology.models import Technology
from matchspecit.technology.serializers import TechnologySerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_matchable = serializers.BooleanField()
    technologies = TechnologySerializer(many=True)

    def update(self, instance, validated_data):
        technologies = validated_data.pop('technologies', None)
        instance.is_matchable = validated_data.get('is_matchable', instance.is_matchable)

        instance.save()

        if technologies:
            instance.technologies.clear()

            for technology in technologies:
                instance.technologies.add(
                    Technology.objects.get(id=technology["id"], name=technology["name"])
                )

        return instance

    class Meta:
        model = User
        fields = ("technologies", "is_matchable")
