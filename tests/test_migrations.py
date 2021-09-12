import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from coturn.models import AdminUser, TurnUser
from coturn.settings import coturn_settings


class TestUserTurnAdminFK(TestCase):
    @override_settings(
        COTURN_USER_MODEL="testapp.CustomUser",
        COTURN_USER_MODEL_REQUEST_CALLBACK=(lambda request: request.user),
    )
    def setUp(self):
        return super().setUp()

    def test_admin_user_fk_to_custom_user_model(self):
        """
        Test to ensure admin_user.django_user fk points to the configured model
        set by COTURN_USER_MODEL
        """
        field = AdminUser._meta.get_field("django_user")

        self.assertEqual(field.related_model, coturn_settings.get_user_model())
        self.assertNotEqual(field.related_model, settings.AUTH_USER_MODEL)

    def test_admin_user_fk_fallback_to_auth_user_model(self):
        """
        Test to ensure admin_user.django_user fk points to the fallback AUTH_USER_MODEL
        when COTURN_USER_MODEL is not set
        """
        # assert COTURN_USER_MODEL has not been set
        with pytest.raises(AttributeError):
            settings.COTURN_USER_MODEL

        field = AdminUser._meta.get_field("django_user")
        self.assertEqual(field.related_model, get_user_model())
