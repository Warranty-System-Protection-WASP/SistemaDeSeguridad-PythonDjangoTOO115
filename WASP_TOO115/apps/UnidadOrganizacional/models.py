from django.db import models

from apps.PuestoDT.models import PuestosDT

# Create your models here.
class UnidadOrganizacional(models.Model):
    idUnidad=models.IntegerField(primary_key=True)
    idPuesto=models.ForeignKey(PuestosDT, on_delete=models.PROTECT)
    nombreUnidad=models.CharField(max_length=50)
    descripUnidad=models.CharField(max_length=200)