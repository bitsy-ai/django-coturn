from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings

from django_coturn.models import TurnSecret

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
        print(args, kwargs)


    def handle(self, *args, **kwargs):
        print(args, kwargs)
        realm = settings.COTURN_REALM
        secret = settings.COTURN_SECRET_KEY
        if len(secret) > 127:
            raise Exception("Coturn's database doesn't support secrets longer than 127 characters")
        for entry in TurnSecret.objects.using('coturn').all():
            entry.delete(using="coturn")
        new_secret = TurnSecret(realm=realm, value=secret)
        new_secret.save(using="coturn")