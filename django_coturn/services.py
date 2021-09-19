
import base64
import hashlib
import hmac
from typing import Tuple
from datetime import timedelta, datetime, timezone
from django.shortcuts import get_object_or_404

from .models import TurnSecret
from .settings import coturn_settings

# TURN REST API authentication strategy 
# https://www.ietf.org/proceedings/87/slides/slides-87-behave-10.pdf

def _get_expiration_timestamp() -> int:
    now = datetime.utcnow()
    expiration_ts = (now + timedelta(seconds=coturn_settings.COTURN_CREDENTIAL_MAX_AGE)).timestamp()
    return int(expiration_ts)

def _create_turn_api_username(email:str) -> str:
    expiration_ts = _get_expiration_timestamp()
    username = "{}:{}".format(email, expiration_ts)
    return username

def _create_turn_api_password(username: str) -> str:
    secret = get_object_or_404(TurnSecret, realm=coturn_settings.COTURN_REALM).first()
    token = hmac.new(secret.value.encode('utf-8'), username.encode('utf-8'), hashlib.sha1)
    encoded_token = base64.b64encode(token.digest()).decode('utf-8')
    return encoded_token

def create_turn_api_credentials(username: str) -> Tuple[str, str]:
    username = _create_turn_api_username(username)
    password = _create_turn_api_password(username)
    return username, password

