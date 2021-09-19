import os
import environ

env = environ.Env()

DEBUG = True
TIME_ZONE = "UTC"
USE_TZ = True
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

db_config = env.db("DATABASE_URL")
db_config["ENGINE"] = "django.db.backends.postgresql"
coturn_db_config = env.db("COTURN_DATABASE_URL")
coturn_db_config["ENGINE"] = "django.db.backends.postgresql"
DATABASES = {"default": db_config, "coturn": coturn_db_config}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ]
        },
    }
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "tests",
    "tests.apps.testapp",
    "django_coturn",
]

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECRET_KEY = "unGPquS03pKnzfQblEpV9KQtFRwgkGaNyS5Ijra7JkM56P9xbE"

AUTH_USER_MODEL = "testapp.CustomUser"
COTURN_REALM = "north.gov"
COTURN_SECRET_KEY = SECRET_KEY
