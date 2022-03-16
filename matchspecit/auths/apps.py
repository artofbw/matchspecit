from django.apps import AppConfig


class AuthsConfig(AppConfig):
    name = "matchspecit.auths"

    def ready(self):
        import matchspecit.auths.signals  # noqa
