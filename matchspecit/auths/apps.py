from django.apps import AppConfig


class AuthsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "matchspecit.auths"

    def ready(self):
        import matchspecit.auths.signals  # noqa
