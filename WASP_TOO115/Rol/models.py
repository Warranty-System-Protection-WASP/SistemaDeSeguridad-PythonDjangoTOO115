from django.db import models

from Empleado.models import Empleado

# Create your models here.
class Rol(models.Model):
    idRol=models.IntegerField(primary_key=True)
    idEmpleado=models.ForeignKey(Empleado, on_delete=models.PROTECT)
    nombreRol=models.CharField(max_length=50)
    descripRol=models.CharField(max_length=200)
    is_activo=models.BooleanField()

class OpcionCrud(models.Model):
    idOpcion=models.IntegerField(primary_key=True)
    numCrud=models.IntegerField()    
    descripCrud=models.CharField(max_length=100)

class RolOpcion(models.Model):
    idOpcion=models.ForeignKey(OpcionCrud, on_delete=models.PROTECT)
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)