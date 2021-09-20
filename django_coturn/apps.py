from django.apps import AppConfig


class DjangoCoturnConfig(AppConfig):
    name = "django_coturn"
    def ready(self):
        try:
            import django_coturn.signals  # noqa F401
        except ImportError:
            pass