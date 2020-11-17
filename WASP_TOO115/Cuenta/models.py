from django.db import models

# Create your models here.
class EstadisticaCuenta(models.Model):
    idEstadisticas=models.IntegerField(primary_key=True)
    cambioClave=models.IntegerField()
    cambioRol=models.IntegerField()

class Cuenta(models.Model):
    nomUsuario=models.CharField(max_length=15, primary_key=True)
    clave=models.CharField(max_length=12)
    idEstadisticas=models.ForeignKey(EstadisticaCuenta,on_delete=models.PROTECT)
    passcode=models.CharField(max_length=6)
    is_bloqueado=models.BooleanField()

class Pregunta(models.Model):
    numPregunta=models.IntegerField(primary_key=True)
    pregunta=models.CharField(max_length=75)  
    respuesta=models.CharField(max_length=75)

class BancoPregunta(models.Model):    
    nomUsuario=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    numPregunta=models.ForeignKey(Pregunta, on_delete=models.PROTECT)