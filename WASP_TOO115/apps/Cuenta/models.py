from django.db import models

# Create your models here.
class EstadisticaCuenta(models.Model):
    idEstadisticas=models.IntegerField(primary_key=True)
    cambioClave=models.IntegerField()
    cambioRol=models.IntegerField()

class Cuenta(models.Model):
    #Referente al Usuario:
    nomUsuario=models.CharField(max_length=15, primary_key=True)
    clave=models.CharField(max_length=12)
    idEstadisticas=models.ForeignKey(EstadisticaCuenta,on_delete=models.PROTECT)
    passcode=models.CharField(max_length=6)
    is_bloqueado=models.BooleanField()
    #Referente al Empleado:
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

class Pregunta(models.Model):
    numPregunta=models.IntegerField(primary_key=True)
    pregunta=models.CharField(max_length=75)  
    respuesta=models.CharField(max_length=75)

class BancoPregunta(models.Model):    
    nomUsuario=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    numPregunta=models.ForeignKey(Pregunta, on_delete=models.PROTECT)

class Solicitud(models.Model):
    idSolicitud=models.IntegerField(primary_key=True)    
    idEmpleado=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    tipoSolicitud=models.CharField(max_length=50)
    estadoSolicitud=models.BooleanField()