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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy, reverse
from django.core.cache import cache
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
import uuid
from uuid import uuid4
from django.db.models import F

# Create your views here.

def instancia():
    if cache.get('intento') == None:
        cache.add('intento',1)

def instancia_data(usuario):
    data = None
    if data == None:
        try:
            data = EstadisticaCuenta.objects.get(cuenta = usuario)
        except EstadisticaCuenta.DoesNotExist:
            data = EstadisticaCuenta(cuenta = usuario, cambioClave = 0, cambioRol = 0, bloqueos = 0)
            data.save()
    return data

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
        estadisticas = EstadisticaCuenta.objects.filter(cuenta = usuario)
        objeto = serializers.serialize('json', estadisticas)
        context = {'form':usuario, 'bitacora':roles, 'estadisticas':objeto}
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
            rol = Rol.objects.all()
            unidad = UnidadOrganizacional.objects.all()
            rol_usuario = RolUsuario.objects.filter(is_activo=True).order_by('idRol')
            data_rol = serializers.serialize('json', rol)
            data_unidad = serializers.serialize('json', unidad)
            data_rol_usuario = serializers.serialize('json', rol_usuario)
            context = {'usuarios':usuario, 'bloqueados':usuario_bloqueado, 'solicitudes':solicitud, 'admin':token, 'data_rol':data_rol, 'data_unidad': data_unidad, 'data_rol_usuario':data_rol_usuario}
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
                    estadistica = instancia_data(usuario)
                    estadistica.cambioRol += 1
                    estadistica.save()
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
        estadistica = instancia_data(usuario)
        estadistica.bloqueos += 1
        estadistica.save()
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
        user.salario = 0.0
        return super(SignUp, self).form_valid(form)

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
    success_url = reverse_lazy('Cuenta:index usuarios')

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
        instancia()
        username = request.POST.get('nombre')
        password = request.POST.get('contra')
        u = Usuario.objects.filter(nomUsuario=username).only('nomUsuario').first()
        nc = Usuario.objects.filter(nomUsuario=u).values('nombre', 'apellido').first()
        # Verificamos las credenciales del usuario
        user = authenticate(request, username=username, password=password)
        # Si existe un usuario con ese nombre y contraseña
        if user is not None:
            cache.set('intento',1)
            if user.is_bloqueado:
                return render(request, '403_2.html')
            else:
                if user.password_change_date is not None:
                    hoy = datetime.now(timezone.utc)
                    pp = user.password_change_date
                    restaTiempo = hoy - user.password_change_date
                    if  restaTiempo > timedelta(seconds=180): #Para comprobar si el tiempo desde que se cambió la contra aún es válido
                        contraExpirada = True
                        print("SOLO ESTOY COMPROBANDO EL PasswordChange 1:", user.password_change_date, 'Tiempo:', restaTiempo)
                        # Hacemos el login manualmente
                        login(request, user)
                        # Y le redireccionamos a la portada
                        return HttpResponseRedirect(reverse_lazy('Cuenta:force_password_change'))
                    else:
                        print("SOLO ESTOY COMPROBANDO EL PasswordChange 2: ", user.password_change_date, 'Tiempo:', restaTiempo)
                        # Hacemos el login manualmente
                        login(request, user)
                        # Y le redireccionamos a la portada
                        return redirect('/')
                else:
                    print("SOLO ESTOY COMPROBANDO EL PasswordChange EN NONE", user.password_change_date)
                    login(request, user)
                    # AQUÍ SE LE VA A REDIRIGIR A UNA PANTALLA PARA EL CAMBIO DE CONTRA Y OTRAS CONFIGURACIONES
                    return HttpResponseRedirect(reverse_lazy('Cuenta:first_password_change'))
        else:
            if cache.get('intento') <3:
                falloContra = Usuario.objects.filter(nomUsuario=u).values('contadorIntentos', 'is_bloqueado') #Voy a recuperar para la lógica del bloqueo de cuenta
                messages.error(request, "Contraseña incorrecta")
                print(cache.get('intento'))
                cache.incr('intento')
                return render(request, 'cuenta/Contraseña.html', {'u': u, 'nc': nc})
            else:
                cache.set('intento',1)
                usb = Usuario.objects.get(nomUsuario=username)
                usb.is_bloqueado=True
                estadistica = instancia_data(usb)
                estadistica.bloqueos += 1
                estadistica.save()
                usb.save()
                return render(request, '403_2.html')
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
        usuario = Usuario.objects.get(nomUsuario = self.request.user)
        estadistica = instancia_data(usuario)
        estadistica.cambioClave += 1
        estadistica.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


####Para cambio de contraseña en primer inicio de sesión####
class FirstPasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('Cuenta:form preguntas')
    template_name = 'cuenta/primercambio.html'

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

class ForcePasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'cuenta/cambio_estricto.html'

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
        usuario = Usuario.objects.get(nomUsuario = self.request.user)
        estadistica = instancia_data(usuario)
        estadistica.cambioClave += 1
        estadistica.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

def formulario_autenticacion(request):
    if request.method == 'GET':
        preguntas = Pregunta.objects.all()
        datos = serializers.serialize('json',preguntas)
        context = {'preguntas':datos}
        return render(request, 'Cuenta/Preguntas.html', context)

    if request.method == 'POST':
        if 'respuesta1' in request.POST:
            if 'respuesta2' in request.POST:
                if 'respuesta3' in request.POST:
                    p1 = Pregunta.objects.get(numPregunta = 1)
                    p2 = Pregunta.objects.get(numPregunta = 2)
                    p3 = Pregunta.objects.get(numPregunta = 3)
                    p4 = Pregunta.objects.get(numPregunta = 4)
                    p5 = Pregunta.objects.get(numPregunta = 5)
                    p6 = Pregunta.objects.get(numPregunta = 6)
                    respuesta_1 = request.POST['respuesta1']
                    respuesta_2 = request.POST['respuesta2']
                    respuesta_3 = request.POST['respuesta3']
                    respuesta_4 = request.POST['respuesta4']
                    respuesta_5 = request.POST['respuesta5']
                    respuesta_6 = request.POST['respuesta6']
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p1, respuesta = respuesta_1)
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p2, respuesta = respuesta_2)
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p3, respuesta = respuesta_3)
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p4, respuesta = respuesta_4)
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p5, respuesta = respuesta_5)
                    BancoPregunta.objects.create(nomUsuario = request.user, numPregunta = p6, respuesta = respuesta_6)
                    return HttpResponse('success')
                else:
                    return HttpResponse('fail')
            else:
                return HttpResponse('fail')
        else:
            return HttpResponse('fail')

class CuentaUser(TemplateView):
    template_name = 'cuenta/CuentaUsuario.html'

def Passcode(request):
    if request.method == "POST":
        u = request.POST.get('cuentaUsuario')
        existeCuenta = Usuario.objects.filter(nomUsuario=u).only('nomUsuario')
        if existeCuenta.count() != 0:
            nc = Usuario.objects.filter(nomUsuario=u).values('nombre', 'apellido').first()
            #preguntaU = BancoPregunta.objects.filter(nomUsuario=u)
            preguntaU = Pregunta.objects.all()
            return render(request, 'cuenta/Passcode.html', {'u': u, 'nc':nc, 'preguntaU':preguntaU})
        else:
            messages.error(request, "No existe ninguna cuenta con ese nombre de usuario")
            return HttpResponseRedirect(reverse_lazy('CuentaUsuario'))
    else:
        return HttpResponseRedirect(reverse_lazy('CuentaUsuario'))

def Reset(request):
    if request.method == 'POST':
        # Recuperamos el nombre de usuario (Cuenta)
        username = request.POST.get('nombre')
        passc = request.POST.get('passcode')
        prU = request.POST.get('pregunta')
        rU = request.POST.get('respuesta')
        u = Usuario.objects.filter(nomUsuario=username).only('nomUsuario').first()
        emailReset = Usuario.objects.filter(nomUsuario=username).values('correo')
        eR = emailReset.get()
        emailR = eR.get('correo')
        bancoPregunta = BancoPregunta.objects.filter(nomUsuario=username).filter(numPregunta=prU).filter(respuesta=rU).values().first()
        passcodeBD = Usuario.objects.filter(nomUsuario=username).values('passcode')
        pBD = passcodeBD.get()
        passcodeUsuarioBD = pBD.get('passcode')
        nc = Usuario.objects.filter(nomUsuario=u).values('nombre', 'apellido').first()
        preguntaU = Pregunta.objects.all()
        verificar = pbkdf2_sha256.verify(passc, passcodeUsuarioBD) #Retorna un boolean
        if verificar == True and bancoPregunta is not None:
            try:
                URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
                too = uuid.uuid4()
                tk = Usuario.objects.filter(nomUsuario=username).values('token')
                tk.update(token=too)
                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                print(mailServer.ehlo())
                mailServer.starttls()
                print(mailServer.ehlo())
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                print('Conectado...')
                #Construcción del mensaje
                mensaje = MIMEMultipart()
                mensaje['From'] = settings.EMAIL_HOST_USER
                mensaje['To'] = emailR
                mensaje['Subject'] = 'Resetear contraseña'
                textoInicial = '\nEnlace temporal para resetear contraseña'
                linkReset = '\nhttp://{}/Reset/Password/{}/'.format(URL, str(too))
                parte0 = MIMEText(textoInicial, 'plain')
                parte1 = MIMEText(linkReset, 'plain')
                mensaje.attach(parte0)
                mensaje.attach(parte1)
                mailServer.sendmail(settings.EMAIL_HOST_USER, emailR, mensaje.as_string())
                print('Correo enviado correctamente')
            except Exception as e:
                print(e)
            return redirect('/')
        else:
            messages.error(request, "Passcode o respuesta a pregunta incorrecta")
            return render(request, 'cuenta/Passcode.html', {'u': u, 'nc': nc, 'preguntaU':preguntaU})
    else:
        return HttpResponseRedirect(reverse_lazy('CuentaUsuario'))

class ResetPassword(FormView):
    form_class = ResetPasswordForm
    template_name = 'cuenta/ResetPassword.html'
    success_url = reverse_lazy('Login')

    def get(self, request, *args, **kwargs):
        token =self.kwargs['token']
        if Usuario.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def form_valid(self, request, *args, **kwargs):
        form = ResetPasswordForm(data=self.request.POST)
        if form.is_valid():
            upass = Usuario.objects.get(token=self.kwargs['token'])
            upass.set_password(form.cleaned_data['password'])
            upass.token = uuid.uuid4()
            upass.password_change_date = datetime.now(timezone.utc)
            upass.is_bloqueado=False
            upass.save()
            estadistica = instancia_data(upass)
            estadistica.cambioClave += 1
            estadistica.save()
            return redirect('NombreUsuario')
