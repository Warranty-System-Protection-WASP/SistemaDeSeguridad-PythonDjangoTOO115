# Generated by Django 3.0.7 on 2020-12-04 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UnidadOrganizacional', '0003_auto_20201203_2031'),
        ('Rol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='unidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='UnidadOrganizacional.UnidadOrganizacional'),
            preserve_default=False,
        ),
    ]
