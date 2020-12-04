from django.db import models

# Create your models here.
class UnidadOrganizacional(models.Model):
    idUnidad=models.AutoField(primary_key=True)
    #idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)
    nombreUnidad=models.CharField(max_length=50)
    descripUnidad=models.CharField(max_length=200)
