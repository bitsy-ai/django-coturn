from collections.abc import Callable
import logging

import hmac
import hashlib

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from django_coturn.services import (
    delete_turn_secrets, 
    create_turn_secret,
    get_or_update_turn_admin,
    get_or_update_turn_user
)

logger = logging.getLogger(__name__)

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        subparsers = parser.add_subparsers(
            title="subcommands", dest="subcommand", required=True
        )

        secret_cmd_parser = subparsers.add_parser("turn_secret")
        secret_cmd_parser.set_defaults(subcommand=self.handle_turn_secret)

        turn_admin_parser = subparsers.add_parser("turn_admin")
        turn_admin_parser.set_defaults(subcommand=self.handle_turn_admin)

        turn_user_parser = subparsers.add_parser("turn_user")
        turn_user_parser.set_defaults(subcommand=self.handle_turn_user)

    def handle_turn_user(self, *args, **kwargs):
        for user in User.objects.all():
            turn_user = get_or_update_turn_user(user)
            self.stdout.write(f"Created {turn_user} from {user}")

    def handle_turn_secret(self, *args, **kwargs):
        delete_turn_secrets()
        new_secret = create_turn_secret()
        self.stdout.write(f"Created {new_secret} from COTURN_SECRET_KEY")

    def handle_turn_admin(self, *args, **kwargs):
        for user in User.objects.filter(is_superuser=True).all():
            turn_admin = get_or_update_turn_admin(user)
            self.stdout.write(f"Created {turn_admin} from {user}")

    def handle(self, subcommand: Callable, *args, **kwargs):
        return subcommand(*args, **kwargs)