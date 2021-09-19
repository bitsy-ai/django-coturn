from collections.abc import Callable
import logging

from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from django_coturn.models import TurnSecret


logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        subparsers = parser.add_subparsers(
            title="subcommands",
            dest="subcommand",
            required=True
        )

        secret_cmd_parser = subparsers.add_parser("turn_secret")
        secret_cmd_parser.set_defaults(subcommand=self.handle_turn_secret)

    def handle_turn_secret(self, *args, **kwargs):
        realm = settings.COTURN_REALM
        secret = settings.COTURN_SECRET_KEY
        for s in TurnSecret.objects.using('coturn').all():
            print(f"Deleting {s}")
            s.delete(using="coturn")
        new_secret = TurnSecret(realm=realm, value=secret)
        new_secret.save(using="coturn")
        print(f"Created {new_secret} from COTURN_SECRET_KEY")


    def handle(self, subcommand: Callable, *args, **kwargs):
        return subcommand(*args, **kwargs)

