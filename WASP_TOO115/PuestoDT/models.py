from django.db import models

from Rol.models import Rol

# Create your models here.
class PuestosDT(models.Model):
    idPuesto=models.IntegerField(primary_key=True)    
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)
    nombrePuesto=models.CharField(max_length=50)
    descripPuesto=models.CharField(max_length=200)