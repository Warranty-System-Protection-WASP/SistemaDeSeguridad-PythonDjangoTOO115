from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic import ListView , DetailView
from django.contrib.auth.models import BaseUserManager
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from passlib.hash import pbkdf2_sha256 #Para encriptación de passcode
from django import forms
from .models import *
from .forms import *

# Create your views here.

#CRUD de Departamento

class CrearDepartamento(SuccessMessageMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'cuenta/CrearDepartamento.html'
    success_url = reverse_lazy('Cuenta:AdministrarDepartamentos')
    success_message = 'Departamento creado con éxito'

class EditarDepartamento(SuccessMessageMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'cuenta/CrearDepartamento.html'
    success_url = reverse_lazy('Cuenta:AdministrarDepartamentos')
    success_message = 'Departamento editado con éxito'

class EliminarDepartamento(DeleteView):
    model = Departamento
    form_class = DepartamentoForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarDepartamentos')

class AdministrarDepartamentos(ListView):
    model = Departamento
    template_name = 'cuenta/AdministrarDepartamentos.html'

#CRUD de Municipios
class CrearMunicipio(SuccessMessageMixin, CreateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'cuenta/CrearMunicipio.html'
    success_url = reverse_lazy('Cuenta:AdministrarMunicipios')
    success_message = 'Municipio creado con éxito'

class EditarMunicipio(SuccessMessageMixin, UpdateView):
    model = Municipio
    form_class = MunicipioForm
    template_name = 'cuenta/CrearMunicipio.html'
    success_url = reverse_lazy('Cuenta:AdministrarMunicipios')
    success_message = 'Municipio editado con éxito'

class EliminarMunicipio(DeleteView):
    model = Municipio
    form_class = MunicipioForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarMunicipios')

class AdministrarMunicipios(ListView):
    model = Municipio
    template_name = 'cuenta/AdministrarMunicipios.html'
    context_object_name = 'Municipios'

#Solicitud de SignUp
class SignUp(SuccessMessageMixin, CreateView):
    model = Usuario
    form_class = SignUpForm
    template_name = 'cuenta/SignUp.html'
    success_url = reverse_lazy('Cuenta:Solicitudes')
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
        muni = Municipio.objects.filter(idMunicipio=mun).filter(departamento=dep).only('nomMunicipio').first()
        depa = Departamento.objects.filter(idDepartamento=dep).only('nomDepartamento').first()
        user.direccion = user.calle + ", " + user.colonia + ", Casa #" + str(user.numCasa) + ", " + str(muni) + ", " + str(depa)
        passcodeHash = user.passcode #Obtiene el passcode ingresado en texto plano
        hash= pbkdf2_sha256.hash(passcodeHash) #Encripta el passcode
        user.passcode = hash #Para guardar encriptado el passcode en la BD
        '''
        #Lo dejo para prueba... lo ocuparé después en el restablecimiento de contraseña
        verificar = pbkdf2_sha256.verify(passcodeHash, hash)
        print(verificar)
        verificar = pbkdf2_sha256.verify("3451", hash)
        print(verificar)
        '''
        user.salario = 0.0
        return super(SignUp, self).form_valid(form)

#Gestión de Solicitudes
class AdministrarSolicitudes(ListView):
    model = Usuario
    template_name = 'cuenta/AdministrarSolicitudes.html'
    context_object_name = 'Solicitudes'

class EliminarSolicitud(DeleteView):
    model = Usuario
    form_class = SignUpForm
    def get_success_url(self):
        return reverse_lazy('Cuenta:AdministrarSolicitudes')

class Aprobar(SuccessMessageMixin, UpdateView):
    model = Usuario
    form_class = AprobarForm
    template_name = 'cuenta/Aprobar.html'
    success_url = reverse_lazy('Cuenta:Solicitudes')
    def form_valid(self, form):
        user=form.save(commit=False)
        if user.solicitud == 'A':
            password = BaseUserManager().make_random_password(12)
            user.set_password(password)
            print("Password que mandaré por correo:", password) #Prueba
            user.is_active = True
        return super(Aprobar, self).form_valid(form)

'''
def NameUser(request):

    return render(request, 'cuenta/nomUsuario.html', {})
'''

class Login(FormView):
    template_name = "cuenta/Login.html"
    form_class = LoginForm
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwards):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwards)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
