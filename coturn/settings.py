from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model


class CoturnSettings:
    def get_user_model_string(self) -> str:
        """Get the configured subscriber model as a module path string."""
        return getattr(settings, "COTURN_USER_MODEL", settings.AUTH_USER_MODEL)

    def get_user_model(self) -> Model:
        """
        Attempt to read settings.COTURN_USER_MODEL.
        This methods falls back to AUTH_USER_MODEL if COTURN_USER_MODEL is not set.
        Returns the subscriber model that is active in this project.
        """
        model_name = self.get_user_model_string()

        # Attempt a Django 1.7 app lookup
        try:
            user_model = django_apps.get_model(model_name)
        except ValueError:
            raise ImproperlyConfigured(
                "COTURN_USER_MODEL must be of the form 'app_label.model_name'."
            )
        except LookupError:
            raise ImproperlyConfigured(
                "COTURN_USER_MODEL refers to model '{model}' "
                "that has not been installed.".format(model=model_name)
            )

        return user_model


django_coturn_settings = CoturnSettings()
