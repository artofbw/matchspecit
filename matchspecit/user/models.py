from django.contrib.auth.models import AbstractUser
from django.db import models

from matchspecit.technology.models import Technology


class User(AbstractUser):
    description = models.TextField("description", blank=True, null=True)
    is_matchable = models.BooleanField("matchable", default=True)
    technologies = models.ManyToManyField(Technology, related_name="technologies")

    def __str__(self):
        return self.username

    def delete(self):
        self.is_active = False
        self.is_matchable = False

        self.save()
