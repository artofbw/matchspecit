from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from matchspecit.project.models import Project

User = get_user_model()


class Match(models.Model):
    user = models.ForeignKey(User, verbose_name="użytkownik", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name="projekt", on_delete=models.CASCADE)
    match_percent = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="spasowanie procentowe")
    project_owner_approved = models.BooleanField("akceptacja własciciela projektu", blank=True, default=None)
    specialist_approved = models.BooleanField("akceptacja specjalisty IT", blank=True, default=None)
    created_at = models.DateTimeField("data utworzenia", default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "project"], name="unique match")]

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
