from django.db import models

from apps.Cuenta.models import Usuario

# Create your models here.
class Rol(models.Model):
    nombreRol=models.CharField(max_length=50)
    descripRol=models.CharField(max_length=200)

class OpcionCrud(models.Model):
    numCrud=models.IntegerField()
    descripCrud=models.CharField(max_length=100)

class RolOpcion(models.Model):
    idOpcion=models.ForeignKey(OpcionCrud, on_delete=models.PROTECT)
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)

class RolUsuario(models.Model):
    idEmpleado=models.ForeignKey(Usuario, on_delete=models.PROTECT)
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)
    is_activo=models.BooleanField()
    fecha_inicio=models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin=models.DateField(auto_now=False, auto_now_add=False)
    #FechaInicio, creo que debe ir según el ejemplo del ingeniero a mi pregunta
    #FechaFin, creo que debe ir según el ejemplo del ingeniero a mi pregunta
