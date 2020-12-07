from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import BaseUserManager
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from passlib.hash import pbkdf2_sha256 #Para encriptación de passcode
from django import forms
from apps.UnidadOrganizacional.models import UnidadOrganizacional
from .models import *
from .forms import *

from apps.Rol.forms import rol_form
from apps.Rol.models import RolUsuario, RolOpcion, Rol, OpcionCrud
from apps.Cuenta.models import Usuario

from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from django.conf import settings

# Create your views here.
def verificar_permiso(request, permiso):
    valor = False

    usuario = Usuario.objects.get(nomUsuario = request.user)
    roluser = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
    puesto = Rol.objects.get(id = roluser.idRol.id)
    opciones = RolOpcion.objects.filter(idRol = puesto)
    cruds = []
    for obj in opciones:
        item = OpcionCrud.objects.get(id = obj.idOpcion.id)
        cruds.append(item)
    acceso = serializers.serialize('json', cruds)

    usuario = Usuario.objects.get(nomUsuario = request.user)
    roluser = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
    puesto = Rol.objects.get(id = roluser.idRol.id)
    opciones = RolOpcion.objects.filter(idRol = puesto)
    try:
        for obj in opciones:
            item = OpcionCrud.objects.get(id = obj.idOpcion.id)
            if item.numCrud == permiso:
                valor = True
                break
        return valor
    except ObjectDoesNotExist:
        return False

@login_required(login_url='Login')
def detalle_usuario(request, username):
    if verificar_permiso(request, 31):
        usuario = Usuario.objects.get(nomUsuario = username)
        roles = RolUsuario.objects.filter(idEmpleado = usuario).order_by('-is_activo')
        context = {'form':usuario, 'bitacora':roles}
        return render(request, 'Usuarios/detalle_usuario.html', context)
    else:
        return render(request, '403.html')

@login_required(login_url='Login')
def index_usuarios(request):
    if verificar_permiso(request, 31):
        usuario = Usuario.objects.filter(is_bloqueado=False)
        usuario_bloqueado = Usuario.objects.filter(is_bloqueado=True)
        solicitud = Usuario.objects.filter(solicitud = 'P')
        usuario2 = Usuario.objects.get(nomUsuario = request.user)
        token = False
        if usuario2.nomUsuario == 'admin':
            token = True
            context = {'usuarios':usuario, 'bloqueados':usuario_bloqueado, 'solicitudes':solicitud, 'admin':token}
            return render(request, 'Usuarios/index_usuarios.html', context)
        else:
            token = False
            context = {'usuarios':usuario, 'bloqueados':usuario_bloqueado, 'solicitudes':solicitud, 'admin':token}
            return render(request, 'Usuarios/index_usuarios.html', context)
    else:
        return render(request, '403.html')

@login_required(login_url='Login')
def edit_usuario(request, username):
    if verificar_permiso(request, 33):
        usuario = Usuario.objects.get(nomUsuario = username)
        puesto = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
        rol = Rol.objects.filter(id = puesto.idRol.id)
        for r in rol:
            unidad = UnidadOrganizacional.objects.filter(idUnidad = r.unidad.idUnidad)
        roles = Rol.objects.all()
        unidades = UnidadOrganizacional.objects.all()
        objeto_rol = serializers.serialize('json', rol)
        objeto_unidad = serializers.serialize('json', unidad)
        if request.method == 'GET':
            form = usuario_form(instance = usuario)
            return render(request, 'Usuarios/form_usuario.html', {'form':form, 'roles':roles, 'unidades':unidades, 'data_rol':objeto_rol, 'data_unidad':objeto_unidad})
        else:
            form = usuario_form(request.POST, instance = usuario)
            if form.is_valid():
                form.save()
                arg = request.POST.get('puestoUsuario')
                print(arg)
                result = Rol.objects.get(id = arg)
                if result.id != puesto.idRol.id:
                    now = datetime.now()
                    puesto.is_activo = False
                    puesto.fecha_fin = now.date()
                    puesto.save()
                    nuevo = RolUsuario(idEmpleado = usuario, idRol = result, is_activo = True, fecha_inicio = now.date())
                    nuevo.save()
            return redirect('Cuenta:index usuarios')
    else:
        return render(request, '403.html')

@login_required(login_url='Login')
def bloquear_usuario(request, username):
    if verificar_permiso(request, 34):
        usuario = Usuario.objects.get(nomUsuario = username)
        usuario.is_bloqueado = True
        usuario.save()
        return redirect('Cuenta:index usuarios')
    else:
        return render(request, '403.html')

@login_required(login_url='Login')
def desbloquear_usuario(request, username):
    if verificar_permiso(request, 34):
        usuario = Usuario.objects.get(nomUsuario = username)
        usuario.is_bloqueado = False
        usuario.save()
        return redirect('Cuenta:index usuarios')
    else:
        return render(request, '403.html')


#CRUD de Departamento
@method_decorator(login_required, name='dispatch')
class CrearDepartamento(SuccessMessageMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'cuenta/CrearDepartamento.html'
    success_url = reverse_lazy('Cuenta:AdministrarDepartamentos')
    success_message = 'Departamento creado con éxito'

@method_decorator(login_required, name='dispatch')
class EditarDepartamento(SuccessMessageMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'cuenta/CrearDepartamento.html'
    success_url = reverse_lazy('Cuenta:AdministrarDepartamentos')
    success_message = 'Departamento editado con éxito'

@method_decorator(login_required, name='dispatch')
class EliminarDepartamento(DeleteView):
    model = Departamento
    form_class = DepartamentoForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarDepartamentos')

@method_decorator(login_required, name='dispatch')
class AdministrarDepartamentos(ListView):
    model = Departamento
    template_name = 'cuenta/AdministrarDepartamentos.html'

#CRUD de Municipios
@method_decorator(login_required, name='dispatch')
class CrearMunicipio(SuccessMessageMixin, CreateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'cuenta/CrearMunicipio.html'
    success_url = reverse_lazy('Cuenta:AdministrarMunicipios')
    success_message = 'Municipio creado con éxito'

@method_decorator(login_required, name='dispatch')
class EditarMunicipio(SuccessMessageMixin, UpdateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'cuenta/CrearMunicipio.html'
    success_url = reverse_lazy('Cuenta:AdministrarMunicipios')
    success_message = 'Municipio editado con éxito'

@method_decorator(login_required, name='dispatch')
class EliminarMunicipio(DeleteView):
    model = Municipio
    form_class = MunicipioForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarMunicipios')

@method_decorator(login_required, name='dispatch')
class AdministrarMunicipios(ListView):
    model = Municipio
    template_name = 'cuenta/AdministrarMunicipios.html'
    context_object_name = 'Municipios'

#Solicitud de SignUp
class SignUp(SuccessMessageMixin, CreateView):
    model = Usuario
    form_class = SignUpForm
    template_name = 'cuenta/SignUp.html'
    success_url = reverse_lazy('index')
    success_message = 'Usuario creado con éxito'

    def form_valid(self, form):
        user=form.save(commit=False)
        stringApellidos = user.apellido
        apellidos = stringApellidos.split(' ')
        primeraLetraApellido = ''
        for a in apellidos:
            primeraLetraApellido += a[0]#Obtiene la primera letra de cada apellido
        #Generación de nombre de usuario a través de la concatenación de la
        #primera letra de cada apellido con el dui
        nomU = primeraLetraApellido + user.dui
        user.nomUsuario = nomU
        if self.request.method == 'POST':
            mun = self.request.POST.get('cbomunicipio')
            dep = self.request.POST.get('cbodepartamento')
            muni = Municipio.objects.filter(idMunicipio=mun, departamento=dep).only('idMunicipio').first()
            user.municipio = muni
        passcodeHash = user.passcode #Obtiene el passcode ingresado en texto plano
        hash= pbkdf2_sha256.hash(passcodeHash) #Encripta el passcode
        user.passcode = hash #Para guardar encriptado el passcode en la BD

        #Lo dejo para prueba... lo ocuparé después en el restablecimiento de contraseña
        verificar = pbkdf2_sha256.verify(passcodeHash, hash)
        print(verificar)
        verificar = pbkdf2_sha256.verify("3451", hash)
        print(verificar)

        user.salario = 0.0
        return super(SignUp, self).form_valid(form)

#Gestión de Solicitudes
#@method_decorator(login_required, name='dispatch')
'''class AdministrarSolicitudes(ListView):
    model = Usuario
    template_name = 'cuenta/AdministrarSolicitudes.html'
    context_object_name = 'Solicitudes'
'''
@method_decorator(login_required, name='dispatch')
class EliminarSolicitud(DeleteView):
    model = Usuario
    form_class = SignUpForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarSolicitudes')

@method_decorator(login_required, name='dispatch')
class Aprobar(SuccessMessageMixin, UpdateView):
    model = Usuario
    form_class = AprobarForm
    template_name = 'cuenta/Aprobar.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(Aprobar, self).get_context_data(**kwargs)
        context['roles'] = Rol.objects.all()
        context['unidades'] = UnidadOrganizacional.objects.all()
        return context

    def form_valid(self, form):
        user=form.save(commit=False)
        if user.solicitud == 'A':
            puesto = self.request.POST.get('puestoUsuario')
            now = datetime.now()
            rol = Rol.objects.get(id=puesto)
            object = RolUsuario.objects.create(idEmpleado=user, idRol=rol, is_activo=True, fecha_inicio=now.date(), fecha_fin='2021-12-04')
            object.save()
            password = get_random_string(length=12)
            try:
                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                print(mailServer.ehlo())
                mailServer.starttls()
                print(mailServer.ehlo())
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                print('Conectado...')
                #Construcción del mensaje
                mensaje = MIMEMultipart('WASP TOO115')
                mensaje['From'] = settings.EMAIL_HOST_USER
                mensaje['To'] = user.correo
                mensaje['Subject'] = 'Aprobación de cuenta WASP'
                nombreU = '\nNombre de usuario: ' + user.nomUsuario
                credencial = '\nPrimera contraseña: ' + password
                linkLogin = '\nhttp://localhost:8000/Login/NomUsuario/'
                textoInicial = 'Su solicitud de creación de cuenta en WASP, ha sido aprobada exitosamente.\nA continuación se le indican sus credenciales para su primer inicio de sesión.'                
                parte0 = MIMEText(textoInicial, 'plain')
                parte1 = MIMEText(nombreU, 'plain')
                parte2 = MIMEText(credencial, 'plain')
                parte3 = MIMEText(linkLogin, 'plain')
                mensaje.attach(parte0)
                mensaje.attach(parte1)
                mensaje.attach(parte2)
                mensaje.attach(parte3)
                mailServer.sendmail(settings.EMAIL_HOST_USER, user.correo, mensaje.as_string())
                print('Correo enviado correctamente')
            except Exception as e:
                print(e)
            user.set_password(password)
            user.is_active = True
        return super(Aprobar, self).form_valid(form)


#DETALLE USUARIO
@method_decorator(login_required, name='dispatch')
class DetalleUsuario(SuccessMessageMixin,DetailView):
       model=Usuario
       template_name = 'cuenta/DetalleUsuario.html'

class NameUser(TemplateView):
    template_name = 'cuenta/Usuario.html'

def Contrasenia(request):
    if request.method == "POST":
        u = request.POST.get('nomUser')
        existeCuenta = Usuario.objects.filter(nomUsuario=u).only('nomUsuario')
        if existeCuenta.count() != 0:
            nc = Usuario.objects.filter(nomUsuario=u).values('nombre', 'apellido').first()
            return render(request, 'cuenta/Contraseña.html', {'u': u, 'nc':nc })
        else:
            messages.error(request, "No existe")
            return HttpResponseRedirect(reverse_lazy('NombreUsuario'))
    else:
        return HttpResponseRedirect(reverse_lazy('NombreUsuario'))

def IniciarSesion(request):
    if request.method == 'POST':
        # Recuperamos las credenciales validadas
        username = request.POST.get('nombre')
        password = request.POST.get('contra')
        u = Usuario.objects.filter(nomUsuario=username).only('nomUsuario').first()
        nc = Usuario.objects.filter(nomUsuario=u).values('nombre', 'apellido').first()
        # Verificamos las credenciales del usuario
        user = authenticate(request, username=username, password=password)
        # Si existe un usuario con ese nombre y contraseña
        if user is not None:
            pL = Usuario.objects.filter(nomUsuario=user).values('last_login') #Para verificar el último login
            primerL = pL.get()
            primerLogin = primerL.get('last_login')
            if primerLogin != None and user.password_change_date is not None:
                hoy = datetime.now(timezone.utc)
                pp = user.password_change_date
                restaTiempo = hoy - user.password_change_date
                if  restaTiempo > timedelta(seconds=180): #Para comprobar si el tiempo desde que se cambió la contra aún es válido
                    contraExpirada = True
                    print("SOLO ESTOY COMPROBANDO EL last_login DIFERENTE DE NONE", primerLogin)
                    # Hacemos el login manualmente
                    login(request, user)
                    # Y le redireccionamos a la portada
                    return HttpResponseRedirect(reverse_lazy('Cuenta:password_change'))
                else:
                    print("SOLO ESTOY COMPROBANDO EL last_login DIFERENTE DE NONE", primerLogin)
                    # Hacemos el login manualmente
                    login(request, user)
                    # Y le redireccionamos a la portada
                    return redirect('/')
            else:
                print("SOLO ESTOY COMPROBANDO EL last_login EN NONE", primerLogin)
                login(request, user)
                # AQUÍ SE LE VA A REDIRIGIR A UNA PANTALLA PARA EL CAMBIO DE CONTRA Y OTRAS CONFIGURACIONES
                #DE MOMENTO EL REDIRECCIONAMIENTO A LA LIST VIEW DE MUNICIPIOS SOLO ES PARA PRUEBA :V
                # RECORDATORIO PARA CUANDO ME DESPIERTE, SÍ FUNCIONA :3
                return HttpResponseRedirect(reverse_lazy('Cuenta:AdministrarMunicipios'))
        else:
            falloContra = Usuario.objects.filter(nomUsuario=u).values('contadorIntentos', 'is_bloqueado') #Voy a recuperar para lalógica del bloqueo de cuenta
            messages.error(request, "Contraseña incorrecta")
            return render(request, 'cuenta/Contraseña.html', {'u': u, 'nc': nc})
        return render(request, 'cuenta/Contraseña.html')
    else:
        return HttpResponseRedirect(reverse_lazy('NombreUsuario'))

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


####Para cambio de contraseña####
class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'cuenta/change_password.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user=form.save(commit=False)
        user.password_change_date = datetime.now(timezone.utc)
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
