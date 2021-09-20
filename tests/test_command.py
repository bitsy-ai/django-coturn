from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class TestCommand(TestCase):

    databases = ("coturn",)

    def test_secret_sync(self):
        out = StringIO()
        call_command('coturn_sync', 'turn_secret', stdout=out)
        assert "Created TurnSecret" in out.getvalue()