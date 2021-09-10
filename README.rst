
=====
Django Coturn
=====

Django Coturn is a Django app to synchronize django admins/users with Coturn's user database. Coturn is an open-source STUN/TURN/ICE server. 

https://github.com/coturn/coturn

Quick start
-----------

1. Add "coturn" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "coturn",
    ]

2. Create an empty `coturn` database

3. Configure the following in your settings.py::

    DATABASES = {
        ... your default and auxilary database configs
        "coturn": env.db("COTURN_DATABASE_URL")
    }

4. Run ``python manage.py migrate`` to create the coturn models.

5. Run ``python manage.py sync_coturn`` to sync users/admin data to coturn tables. You only need to do this once - subsequent updates will be handled by Django signals.
