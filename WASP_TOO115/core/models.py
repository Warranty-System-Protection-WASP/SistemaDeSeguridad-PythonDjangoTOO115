from django.db import models


# Modelos para la base de datos en Oracle 12c (CodeFirst)
# Create your models here.
# El PROTECT se usa para no eliminar los campos
class Pregunta(models.Model):
    numPregunta=models.IntegerField(primary_key=True)
    pregunta=models.CharField(max_length=75)  
    respuesta=models.CharField(max_length=75)  

class EstadisticaCuenta(models.Model):
    idEstadisticas=models.IntegerField(primary_key=True)
    cambioClave=models.IntegerField()
    cambioRol=models.IntegerField()

class Cuenta(models.Model):
    nomUsuario=models.CharField(max_length=15, primary_key=True)
    clave=models.CharField(max_length=12,primary_key=True)
    idEstadisticas=models.ForeignKey(EstadisticaCuenta,on_delete=models.PROTECT)
    passcode=models.CharField(max_length=6)

class BancoPregunta(models.Model):    
    nomUsuario=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    clave=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    numPregunta=models.ForeignKey(Pregunta, on_delete=models.PROTECT)

class OpcionCrud(models.Model):
    idOpcion=models.IntegerField(primary_key=True)
    numCrud=models.IntegerField()    
    descripCrud=models.CharField(max_length=100)

class Empleado(models.Model):
    idEmpleado=models.IntegerField(primary_key=True)
    nomUsuario=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    clave=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    #idERH=models.ForeignKey(ERH, on_delete=models.PROTECT)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    salario=models.DecimalField()
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

class ERH(models.Model):
    idERH=models.IntegerField(primary_key=True)
    idEmpleado=models.ForeignKey(Empleado, on_delete=models.PROTECT)

class Rol(models.Model):
    idRol=models.IntegerField(primary_key=True)
    idEmpleado=models.ForeignKey(Empleado, on_delete=models.PROTECT)
    idERH=models.ForeignKey(ERH, on_delete=models.PROTECT)
    nombreRol=models.CharField(max_length=50)
    descripRol=models.CharField(max_length=200)

class Solicitud(models.Model):
    idSolicitud=models.CharField(primary_key=True)    
    idEmpleado=models.ForeignKey(Empleado, on_delete=models.PROTECT)
    idERH=models.ForeignKey(ERH, on_delete=models.PROTECT)
    tipoSolicitud=models.CharField(max_length=50)
    estadoSolicitud=models.BooleanField()

class RolOpcion(models.Model):
    idOpcion=models.ForeignKey(OpcionCrud, on_delete=models.PROTECT)
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)

class PuestosDT(models.Model):
    idPuesto=models.IntegerField(primary_key=True)    
    idRol=models.ForeignKey(Rol, on_delete=models.PROTECT)
    nombrePuesto=models.CharField(max_length=50)
    descripPuesto=models.CharField(max_length=200)

class UnidadOrganizacional(models.Model):
    idUnidad=models.IntegerField(primary_key=True)
    idPuesto=models.ForeignKey(PuestosDT, on_delete=models.PROTECT)
    nombreUnidad=models.CharField(max_length=50)
    descripUnidad=models.CharField(max_length=200)