# References: https://github.com/coturn/coturn/blob/master/turndb/schema.sql

from django.db import models

from django.contrib.auth.models import AbstractUser

from .settings import coturn_settings


class TurnAdmin(models.Model):
    """
        A coturn admin_user row is created automatically for superusers
    """
    name = models.CharField(unique=True, max_length=32)
    realm = models.CharField(max_length=127, blank=True, null=True)
    password = models.CharField(max_length=127)
    django_user_id = models.BigIntegerField()

    class Meta:
        db_table = "admin_user"
        constraints = (
            models.UniqueConstraint(fields=["realm", "name"], name="unique_admin_username_per_realm"),
            models.UniqueConstraint(fields=["realm", "django_user_id"], name="unique_django_admin_per_realm")
        )
class AllowedPeerIp(models.Model):
    realm = models.CharField(max_length=127, blank=True, null=True)
    ip_range = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = "allowed_peer_ip"
        constraints = (
            models.UniqueConstraint(fields=["realm", "ip_range"], name="unique_allowed_ip_range_realm"),
        )

class DeniedPeerIp(models.Model):
    realm = models.CharField(max_length=127, blank=True, null=True)
    ip_range = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = "denied_peer_ip"
        constraints = (
            models.UniqueConstraint(fields=["realm", "ip_range"], name="unique_denied_ip_range_realm"),
        )

class OauthKey(models.Model):
    kid = models.CharField(unique=True, max_length=128)
    ikm_key = models.CharField(max_length=256)
    timestamp = models.BigIntegerField()
    lifetime = models.IntegerField()
    as_rs_alg = models.CharField(max_length=64)
    realm = models.CharField(max_length=127)

    class Meta:
        db_table = "oauth_key"


class TurnOriginToRealm(models.Model):
    origin = models.CharField(unique=True, max_length=127)
    realm = models.CharField(max_length=127)

    class Meta:
        db_table = "turn_origin_to_realm"


class TurnRealmOption(models.Model):
    realm = models.CharField(max_length=127, blank=True, null=True)
    opt = models.CharField(max_length=32, blank=True, null=True)
    value = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = "turn_realm_option"
        constraints = (
            models.UniqueConstraint(fields=["realm", "opt"], name="unique_opt_per_realm"),
        )

class TurnSecret(models.Model):
    realm = models.CharField(max_length=127)
    value = models.CharField(max_length=127)

    class Meta:
        db_table = "turn_secret"
        constraints = (
            models.UniqueConstraint(
            fields=["realm", "value"], name="unique_value_per_realm"
            ),
        )

class TurnUser(models.Model):
    """
        This data model is only used by Coturn's long-term credential strategy
    """
    realm = models.CharField(max_length=127, blank=True, default="")
    name = models.CharField(max_length=512, blank=True, null=True)
    hmackey = models.CharField(max_length=128, blank=True, null=True)
    django_user_id = models.BigIntegerField()

    class Meta:
        db_table = "turnusers_lt"
        constraints = (
            models.UniqueConstraint(fields=["realm", "name"], name="unique_username_per_realm"),
            models.UniqueConstraint(fields=["realm", "django_user_id"], name="unique_django_user_per_realm")
        )
