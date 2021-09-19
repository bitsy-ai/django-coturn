from collections.abc import Callable
import logging

import hmac
import hashlib

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from django_coturn.models import TurnSecret, TurnAdmin, TurnUser


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
            try:
                u = TurnUser.objects.get(name=user.email)
                print(f"Skipping user with id={user.id} (already exists)")
            except User.DoesNotExist:
                password = User.objects.make_random_password()
                hmackey = hmac.new(
                    settings.COTURN_SECRET_KEY.encode("utf-8"),
                    password.encode("utf-8"),
                    hashlib.sha1,
                )
                hmackey.update(settings.COTURN_REALM.encode("utf-8"))
                u = TurnUser.objects.create(
                    user=user.email,
                    realm=settings.COTURN_REALM,
                    django_user_id=user.id,
                    hmackey=hmackey.hexdigest(),
                )
                print(f"Created turnsusers_lt {u}")

    def handle_turn_secret(self, *args, **kwargs):
        realm = settings.COTURN_REALM
        secret = settings.COTURN_SECRET_KEY
        for s in TurnSecret.objects.using("coturn").all():
            print(f"Deleting {s}")
            s.delete(using="coturn")
        new_secret = TurnSecret(realm=realm, value=secret)
        new_secret.save(using="coturn")
        print(f"Created {new_secret} from COTURN_SECRET_KEY")

    def handle_turn_admin(self, *args, **kwargs):

        for superuser in User.objects.filter(superuser=True).all():
            try:
                a = TurnAdmin.objects.get(name=superuser.email)
                print(f"Skipping turn_admin creation for {superuser.email}")
                if a.django_user_id is None:
                    a.django_user_id = superuser.id
                    a.save()
                    print(
                        f"Updated TURN admin_user {a} django_user_id={a.django_user_id}"
                    )
            except TurnAdmin.DoesNotExist:
                a = TurnAdmin.objects.create(
                    name=superuser.email,
                    django_user_id=superuser.id,
                    password="CHANGEME",
                )

                print(f"Created admin_user {a}")
