from django.test import TestCase

from coturn.services import create_turn_api_credentials

class TestServices(TestCase):

    def test_create_turn_api_credentials(self):
        email = "test-user@test.com"
        username, password = create_turn_api_credentials(email)
        

