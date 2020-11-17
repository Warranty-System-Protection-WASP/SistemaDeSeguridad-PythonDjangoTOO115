from django.db import models

from Cuenta.models import Cuenta

# Create your models here.
class Empleado(models.Model):
    idEmpleado=models.IntegerField(primary_key=True)
    nomUsuario=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    salario=models.DecimalField(max_digits=5, decimal_places=2)
    dui=models.CharField(max_length=50)
    isss=models.CharField(max_length=50)
    nup=models.CharField(max_length=50)
    nit=models.CharField(max_length=50)
    genero=models.CharField(max_length=20)
    estadoCivil=models.CharField(max_length=20)
    departamento=models.CharField(max_length=50)
    municipio=models.CharField(max_length=50)
    correo=models.CharField(max_length=50)
    telefono=models.CharField(max_length=12)

class Solicitud(models.Model):
    idSolicitud=models.IntegerField(primary_key=True)    
    idEmpleado=models.ForeignKey(Empleado, on_delete=models.PROTECT)
    tipoSolicitud=models.CharField(max_length=50)
    estadoSolicitud=models.BooleanField()