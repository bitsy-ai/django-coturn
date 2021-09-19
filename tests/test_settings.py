"""
dj-stripe Migrations Tests
"""
import pytest
from django.conf import settings
from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured

from coturn.settings import coturn_settings


class TestCoturnSettings(TestCase):

    def setUp(self):
        return super().setUp()

    @override_settings(
        COTURN_AUTH_STRATEGY="invalid"
    )
    def test_invalid_auth_strategy(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_AUTH_STRATEGY

    @override_settings(
        COTURN_REALM=None
    )
    def test_invalid_realm(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_REALM

    @override_settings(
        COTURN_SHARED_SECRET=None
    )
    def test_invalid_shared_secret(self):
        with pytest.raises(ImproperlyConfigured):
            coturn_settings.COTURN_SHARED_SECRET