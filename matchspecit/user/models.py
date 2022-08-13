import django.contrib.auth.validators
from django.contrib.auth.models import AbstractUser
from django.db import models

from matchspecit.technology.models import Technology


class User(AbstractUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="last login")
    username = models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username")
    first_name = models.CharField(blank=True, max_length=150, verbose_name="first name")
    last_name = models.CharField(blank=True, max_length=150, verbose_name="last name")
    email = models.EmailField(blank=True, max_length=254, verbose_name="email address")
    is_active = models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of "
                                  "deleting accounts.",
                        verbose_name="active")
    date_joined = models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")

    description = models.TextField("description", blank=True, null=True)
    is_matchable = models.BooleanField("matchable", default=True)
    technologies = models.ManyToManyField(Technology, related_name="users2technologies")

    def __str__(self):
        return self.username

    def delete(self):
        self.is_active = False
        self.is_matchable = False

        self.save()
