# Generated by Django 3.0.7 on 2020-11-28 03:35

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cuenta', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
