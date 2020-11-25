from django.db import models

from apps.Rol.models import Rol

# Create your models here.
class UnidadOrganizacional(models.Model):
    idUnidad=models.IntegerField(primary_key=True)
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)
    nombreUnidad=models.CharField(max_length=50)
    descripUnidad=models.CharField(max_length=200)
