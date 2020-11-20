from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, nomUsuario, passcode, nombre, apellido, fechaNacimiento,
        correo, telefono, dui, nit, isss, nup, salario, genero, estadoCivil, numCasa, calle, colonia, password = None):
        if not  correo:
            raise ValueError('El usuario debe tener un correo')

        usuario = self.model(
            nomUsuario = nomUsuario,
            passcode = passcode,
            nombre=nombre, apellido=apellido,
            fechaNacimiento=fechaNacimiento,
            correo = self.normalize_email(correo),
            telefono=telefono,
            dui=dui,
            nit=nit,
            isss=isss,
            nup=nup,
            salario=salario,genero=genero,
            estadoCivil=estadoCivil,
            numCasa=numCasa,
            calle=numCalle,
            colonia=colonia)
        usuario.set_password(password)
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    EstadoCivil=[
        ('casado', 'Casado'),
        ('soltero', 'Soltero'),
        ('divorciado', 'Divorciado'),
        ('viudo', 'Viudo'),
    ]
    Genero=[
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
        ('indefinido', 'Prefiero no decirlo'),
    ]
    EstadoSolicitud=[
        ('A', 'Aprobada'),
        ('R', 'Rechazada'),
        ('P', 'Pendiente'),
    ]
    #Referente al Usuario:
    nomUsuario=models.CharField(max_length=15, primary_key=True)
    #EstadisticaCuenta no puede ir aquí, porque la misma EstadisticaCuenta se podría asociar a varias cuentas, lo cuál no debe ser
    #idEstadisticas=models.ForeignKey(EstadisticaCuenta,on_delete=models.PROTECT)
    passcode=models.CharField(max_length=4, blank=False)
    is_bloqueado=models.BooleanField(default=False)
    #Llevará la cuenta de intentos fallidos de contraseña
    contadorIntentos = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default=False)
    solicitud = models.CharField(choices=EstadoSolicitud, default='P', max_length=1)
    #Referente al Empleado:
    nombre=models.CharField(max_length=50, blank=False)
    apellido=models.CharField(max_length=50, blank=False)
    fechaNacimiento = models.DateField(blank=False)
    correo = models.EmailField(max_length=255, unique = True)
    telefono=models.CharField(max_length=12, blank=False)
    dui=models.CharField(max_length=9, unique= True, blank=False)
    nit=models.CharField(max_length=14, unique= True, blank=False)
    isss=models.CharField(max_length=9, unique= True, blank=False)
    nup=models.CharField(max_length=12, unique= True, blank=False)
    salario=models.DecimalField(max_digits=5, decimal_places=2)
    genero=models.CharField(choices = Genero, max_length=10)
    estadoCivil=models.CharField(choices = EstadoCivil, max_length=10)
    direccion = models.CharField(max_length=200)
    numCasa = models.PositiveIntegerField(blank=False)
    calle = models.CharField(max_length=50, blank=False)
    colonia = models.CharField(max_length=50, blank=False)
    objects = UserManager()

    USERNAME_FIELD = 'nomUsuario'

    def __str__(self):
        return  self.dui + " " + self.nombre

class Pregunta(models.Model):
    numPregunta=models.IntegerField(primary_key=True)
    pregunta=models.CharField(max_length=75)

class BancoPregunta(models.Model):
    nomUsuario=models.ForeignKey(Usuario, on_delete=models.PROTECT)
    numPregunta=models.ForeignKey(Pregunta, on_delete=models.PROTECT)
    respuesta=models.CharField(max_length=75)

class EstadisticaCuenta(models.Model):
    idEstadisticas=models.AutoField(primary_key=True)
    cuenta = models.ForeignKey(Usuario, on_delete= models.PROTECT)
    cambioClave=models.PositiveIntegerField(default=0)
    cambioRol=models.PositiveIntegerField(default=0)
    bloqueos=models.PositiveIntegerField(default=0)

class Departamento(models.Model):
    idDepartamento = models.AutoField(primary_key=True)
    nomDepartamento = models.CharField(max_length=15)

class Municipio(models.Model):
    idMunicipio = models.AutoField(primary_key = True)
    nomMunicipio = models.CharField(max_length=30)
    departamento = models.ForeignKey(Departamento, on_delete = models.PROTECT)

'''
class Solicitud(models.Model):
    idSolicitud=models.IntegerField(primary_key=True)
    idEmpleado=models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    tipoSolicitud=models.CharField(max_length=50)
    estadoSolicitud=models.BooleanField()
'''