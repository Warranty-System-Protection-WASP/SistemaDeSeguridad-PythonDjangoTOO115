# Generated by Django 3.0.7 on 2020-11-20 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OpcionCrud',
            fields=[
                ('idOpcion', models.IntegerField(primary_key=True, serialize=False)),
                ('numCrud', models.IntegerField()),
                ('descripCrud', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('idRol', models.IntegerField(primary_key=True, serialize=False)),
                ('nombreRol', models.CharField(max_length=50)),
                ('descripRol', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RolUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_activo', models.BooleanField()),
                ('idEmpleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('idRol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Rol.Rol')),
            ],
        ),
        migrations.CreateModel(
            name='RolOpcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idOpcion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Rol.OpcionCrud')),
                ('idRol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Rol.Rol')),
            ],
        ),
    ]
