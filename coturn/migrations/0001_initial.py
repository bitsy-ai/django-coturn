# Generated by Django 3.2.7 on 2021-09-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedPeerIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(blank=True, max_length=127, null=True)),
                ('ip_range', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'allowed_peer_ip',
            },
        ),
        migrations.CreateModel(
            name='DeniedPeerIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(blank=True, max_length=127, null=True)),
                ('ip_range', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'denied_peer_ip',
            },
        ),
        migrations.CreateModel(
            name='OauthKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kid', models.CharField(max_length=128, unique=True)),
                ('ikm_key', models.CharField(max_length=256)),
                ('timestamp', models.BigIntegerField()),
                ('lifetime', models.IntegerField()),
                ('as_rs_alg', models.CharField(max_length=64)),
                ('realm', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'oauth_key',
            },
        ),
        migrations.CreateModel(
            name='TurnAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('realm', models.CharField(blank=True, max_length=127, null=True)),
                ('password', models.CharField(max_length=127)),
                ('django_user_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'admin_user',
            },
        ),
        migrations.CreateModel(
            name='TurnOriginToRealm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=127, unique=True)),
                ('realm', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'turn_origin_to_realm',
            },
        ),
        migrations.CreateModel(
            name='TurnRealmOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(blank=True, max_length=127, null=True)),
                ('opt', models.CharField(blank=True, max_length=32, null=True)),
                ('value', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'turn_realm_option',
            },
        ),
        migrations.CreateModel(
            name='TurnSecret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(max_length=127)),
                ('value', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'turn_secret',
            },
        ),
        migrations.CreateModel(
            name='TurnUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realm', models.CharField(blank=True, default='', max_length=127)),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('hmackey', models.CharField(blank=True, max_length=128, null=True)),
                ('django_user_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'turnusers_lt',
            },
        ),
        migrations.AddConstraint(
            model_name='turnuser',
            constraint=models.UniqueConstraint(fields=('realm', 'name'), name='unique_username_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='turnuser',
            constraint=models.UniqueConstraint(fields=('realm', 'django_user_id'), name='unique_django_user_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='turnsecret',
            constraint=models.UniqueConstraint(fields=('realm', 'value'), name='unique_value_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='turnrealmoption',
            constraint=models.UniqueConstraint(fields=('realm', 'opt'), name='unique_opt_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='turnadmin',
            constraint=models.UniqueConstraint(fields=('realm', 'name'), name='unique_admin_username_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='turnadmin',
            constraint=models.UniqueConstraint(fields=('realm', 'django_user_id'), name='unique_django_admin_per_realm'),
        ),
        migrations.AddConstraint(
            model_name='deniedpeerip',
            constraint=models.UniqueConstraint(fields=('realm', 'ip_range'), name='unique_denied_ip_range_realm'),
        ),
        migrations.AddConstraint(
            model_name='allowedpeerip',
            constraint=models.UniqueConstraint(fields=('realm', 'ip_range'), name='unique_allowed_ip_range_realm'),
        ),
    ]
