"""
dj-stripe Migrations Tests
"""
import string
import random
import pytest
from django.conf import settings
from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured

from django_coturn.settings import coturn_settings


class TestCoturnSettings(TestCase):
    def setUp(self):
        return super().setUp()

    @override_settings(COTURN_AUTH_STRATEGY="invalid")
    def test_invalid_auth_strategy(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_AUTH_STRATEGY

    @override_settings(COTURN_REALM=None, COTURN_SECRET_KEY=None)
    def test_required_settings(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_REALM
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_SECRET_KEY

    @override_settings(
        COTURN_SECRET_KEY="".join(
            random.choices(string.ascii_uppercase + string.digits, k=128)
        )
    )
    def test_invalid_secret_key(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_SECRET_KEY
