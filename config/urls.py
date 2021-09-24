from django.urls import path, include
urlpatterns = [
    path("coturn/", include("django_coturn.urls"))
]