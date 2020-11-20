# Generated by Django 3.0.7 on 2020-11-20 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('idDepartamento', models.AutoField(primary_key=True, serialize=False)),
                ('nomDepartamento', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('numPregunta', models.IntegerField(primary_key=True, serialize=False)),
                ('pregunta', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nomUsuario', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('passcode', models.CharField(max_length=4)),
                ('is_bloqueado', models.BooleanField(default=False)),
                ('contadorIntentos', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('solicitud', models.CharField(choices=[('A', 'Aprobada'), ('R', 'Rechazada'), ('P', 'Pendiente')], default='P', max_length=1)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fechaNacimiento', models.DateField()),
                ('correo', models.EmailField(max_length=255, unique=True)),
                ('telefono', models.CharField(max_length=12)),
                ('dui', models.CharField(max_length=9, unique=True)),
                ('nit', models.CharField(max_length=14, unique=True)),
                ('isss', models.CharField(max_length=9, unique=True)),
                ('nup', models.CharField(max_length=12, unique=True)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=5)),
                ('genero', models.CharField(choices=[('femenino', 'Femenino'), ('masculino', 'Masculino'), ('indefinido', 'Prefiero no decirlo')], max_length=10)),
                ('estadoCivil', models.CharField(choices=[('casado', 'Casado'), ('soltero', 'Soltero'), ('divorciado', 'Divorciado'), ('viudo', 'Viudo')], max_length=10)),
                ('direccion', models.CharField(max_length=200)),
                ('numCasa', models.PositiveIntegerField()),
                ('calle', models.CharField(max_length=50)),
                ('colonia', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('idMunicipio', models.AutoField(primary_key=True, serialize=False)),
                ('nomMunicipio', models.CharField(max_length=30)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Cuenta.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='EstadisticaCuenta',
            fields=[
                ('idEstadisticas', models.AutoField(primary_key=True, serialize=False)),
                ('cambioClave', models.PositiveIntegerField(default=0)),
                ('cambioRol', models.PositiveIntegerField(default=0)),
                ('bloqueos', models.PositiveIntegerField(default=0)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BancoPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=75)),
                ('nomUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('numPregunta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Cuenta.Pregunta')),
            ],
        ),
    ]