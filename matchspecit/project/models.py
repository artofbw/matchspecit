from django.contrib.auth import get_user_model
from matchspecit.technology.models import Technology
from django.db import models

User = get_user_model()


class Project(models.Model):
    title = models.CharField("title", max_length=50)
    description = models.TextField("description", max_length=574)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name="użytkownik", on_delete=models.CASCADE)
    is_matchable = models.BooleanField("matchable", default=True)
    is_finish = models.BooleanField("finish", default=False)
    is_successful = models.BooleanField("successful", default=False)
    is_deleted = models.BooleanField("deleted", default=False)
    technologies = models.ManyToManyField(Technology, related_name="projects2technologies")
    image = models.ImageField(upload_to='files/covers', null=True)

    def __str__(self):
        return self.title

    def delete(self):
        self.is_matchable = False
        self.is_deleted = True

        self.save()
