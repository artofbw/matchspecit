# flake8: noqa
from core.settings_local import *

DEBUG = False
SSL_ENABLED = False

DEBUG_TOOLBAR_CONFIG = {
    # don't show Debug Toolbar in tests
    "SHOW_TOOLBAR_CALLBACK": lambda request: False,
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test.db"),
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
