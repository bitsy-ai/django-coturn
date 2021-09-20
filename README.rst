
==============
Django Coturn
==============

.. image:: https://img.shields.io/pypi/v/django-coturn
.. image:: https://img.shields.io/github/release-date-pre/bitsy-ai/django-coturn
.. image:: https://img.shields.io/pypi/pyversions/django-coturn
.. image:: https://img.shields.io/pypi/djversions/django-coturn
.. image:: https://img.shields.io/pypi/wheel/django-coturn

.. image:: https://img.shields.io/github/workflow/status/bitsy-ai/django-coturn/Test
.. image:: https://img.shields.io/codecov/c/github/bitsy-ai/django-coturn
.. image:: https://img.shields.io/discord/773452324692688956



Django Coturn is a Django app to synchronize django admins/users with Coturn's user database. Coturn is an open-source STUN/TURN/ICE server. 

https://github.com/coturn/coturn

Quick start
-----------

1. Add "coturn" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "django_coturn",
    ]

2. Create an empty `coturn` database

3. Configure the following in your settings.py::

    DATABASES = {
        ... your default and auxilary database configs
        "coturn": env.db("COTURN_DATABASE_URL")
    }

    COTURN_REALM = "turn.example-domain.com"
    COTURN_SECRET_KEY = "127 character secret"

4. Run ``python manage.py migrate`` to create the coturn models.

5. Run ``python manage.py sync_coturn {turn_secret,turn_admin,turn_user}`` to sync users/admin data to coturn tables. You only need to do this once per table - subsequent updates will be handled by Django signals.

Contributor's Guide
--------------------

1. Create a development environment (requires docker & docker-compose)::

    make dev

2. Run tests and generate a coverage report::

    make tests

3. Run `black` linter::

    make lint

