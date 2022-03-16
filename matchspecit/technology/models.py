from django.db import models


class Technology(models.Model):
    name = models.CharField("name", max_length=20, blank=False)

    class Meta:
        verbose_name = "technology"
        verbose_name_plural = "technologies"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique technology",
            )
        ]

    def __str__(self):
        return self.name
