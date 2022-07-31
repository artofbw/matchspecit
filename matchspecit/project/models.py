from django.contrib.auth import get_user_model
from matchspecit.technology.models import Technology
from django.db import models

User = get_user_model()


class Project(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField("title", max_length=50)
    description = models.TextField("description", max_length=574)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    owner = models.ForeignKey(User, verbose_name="użytkownik", on_delete=models.CASCADE)
    is_matchable = models.BooleanField("matchable", blank=True, default=True)
    is_finish = models.BooleanField("finish", blank=True, default=False)
    is_successful = models.BooleanField("successful", blank=True, default=False)
    is_deleted = models.BooleanField("deleted", blank=True, default=False)
    technologies = models.ManyToManyField(Technology, related_name="projects2technologies")
    image = models.ImageField(upload_to='files/covers', blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self):
        self.is_matchable = False
        self.is_deleted = True

        self.save()
