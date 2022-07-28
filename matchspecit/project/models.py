from django.db import models
from multiselectfield import MultiSelectField


class Project(models.Model):
    PROJECT_CHOICES = (
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('Django', 'Django')
    )

    title = models.CharField("title", max_length=50, null = True)
    description = models.TextField("description", blank=True, null=True, max_length=574)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.CharField("owner", max_length=255, null = True)
    is_matchable = models.BooleanField("matchable", default=True)
    is_finish = models.BooleanField("finish", default=True)
    is_successful = models.BooleanField("successful", default=True)
    technologies = MultiSelectField(choices= PROJECT_CHOICES, default=True)
    image = models.ImageField(upload_to='files/covers', null = True)

    def __str__(self):
        return self.title


    def delete(self):
        self.is_matchable = False
        self.is_finish = False
        self.is_successful = False

        self.save()