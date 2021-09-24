from django.urls import path

from .views import create_coturn_credential

app_name = "django_coturn"
urlpatterns = [path("credential", create_coturn_credential)]
