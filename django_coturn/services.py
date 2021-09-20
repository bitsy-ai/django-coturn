import base64
import hashlib
import hmac

import logging
from typing import Tuple
from datetime import timedelta, datetime, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import TurnAdmin, TurnSecret, TurnUser
from .settings import coturn_settings

# TURN REST API authentication strategy
# https://www.ietf.org/proceedings/87/slides/slides-87-behave-10.pdf

logger = logging.getLogger(__name__)
User = get_user_model()

def _get_expiration_timestamp() -> int:
    now = datetime.utcnow()
    expiration_ts = (
        now + timedelta(seconds=coturn_settings.COTURN_CREDENTIAL_MAX_AGE)
    ).timestamp()
    return int(expiration_ts)


def _create_turn_api_username(email: str) -> str:
    expiration_ts = _get_expiration_timestamp()
    username = "{}:{}".format(email, expiration_ts)
    return username


def _create_turn_api_password(username: str) -> str:
    secret = get_object_or_404(TurnSecret, realm=coturn_settings.COTURN_REALM).first()
    token = hmac.new(
        secret.value.encode("utf-8"), username.encode("utf-8"), hashlib.sha1
    )
    encoded_token = base64.b64encode(token.digest()).decode("utf-8")
    return encoded_token


def create_turn_api_credentials(username: str) -> Tuple[str, str]:
    username = _create_turn_api_username(username)
    password = _create_turn_api_password(username)
    return username, password


def create_turn_admin(user: User, default_password="CHANGEME") -> TurnAdmin:
    return TurnAdmin.objects.create(
        name=user.email,
        django_user_id=user.id,
        password=default_password,
    )

def delete_turn_secrets():
    for s in TurnSecret.objects.using("coturn").all():
        s.delete(using="coturn")

def create_turn_secret() -> TurnSecret:
    realm = settings.COTURN_REALM
    secret = settings.COTURN_SECRET_KEY
    new_secret = TurnSecret(realm=realm, value=secret)
    new_secret.save(using="coturn")
    return new_secret

def get_or_update_turn_user(user: User) -> TurnUser:
    try:
        turn_user = TurnUser.objects.get(django_user_id=user.id)
        logger.debug(f"Found existing TurnUser id={turn_user.id} django_user_id={turn_user.django_user_id}")
    except TurnUser.DoesNotExist:
        password = User.objects.make_random_password()
        hmackey = hmac.new(
            settings.COTURN_SECRET_KEY.encode("utf-8"),
            password.encode("utf-8"),
            hashlib.sha1,
        )
        hmackey.update(settings.COTURN_REALM.encode("utf-8"))
        turn_user = TurnUser.objects.create(
            name=user.email,
            realm=settings.COTURN_REALM,
            django_user_id=user.id,
            hmackey=hmackey.hexdigest(),
        )
        logger.debug(f"Created new TurnUser id={turn_user.id} django_user_id={turn_user.django_user_id}")
    return turn_user

def get_or_update_turn_admin(user: User) -> TurnAdmin:
    try:
        turn_admin = TurnAdmin.objects.get(name=user.email)
        if turn_admin.django_user_id is None:
            turn_admin.django_user_id = user.id
            turn_admin.save()
            logger.info(f"Linked TurnAdmin id={turn_admin.id} to django_user_id={turn_admin.django_user_id}")
    except TurnAdmin.DoesNotExist:
        turn_admin = TurnAdmin.objects.create(
            name=user.email,
            django_user_id=user.id,
            password=User.objects.make_random_password(),
        )
    return turn_admin
