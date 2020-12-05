from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

#from apps.Rol.models import Rol, RolOpcion
from apps.Rol.forms import rol_form
from apps.Rol.models import RolUsuario, RolOpcion, Rol
from apps.Cuenta.models import Usuario

import json

# Create your views here.

switches = ["customSwitch1","customSwitch2","customSwitch3","customSwitch4","customSwitch5","customSwitch6","customSwitch7","customSwitch8","customSwitch9","customSwitch10","customSwitch11","customSwitch12"]

def verificar(request):
    usuario = Usuario.objects.get(nomUsuario = request.user)
    roluser = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
    puesto = Rol.objects.get(id = roluser.idRol.id)
    opciones = RolOpcion.objects.filter(idRol = puesto)
    #js_data = "{}"
    acceso = serializers.serialize('json', opciones)
    return {'permisos':acceso}

def verificar_permiso(request, permiso):
    usuario = Usuario.objects.get(nomUsuario = request.user)
    roluser = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
    puesto = Rol.objects.get(id = roluser.idRol.id)
    try:
        opciones = RolOpcion.objects.filter(idOpcion = permiso, idRol = puesto)
        return True
    except ObjectDoesNotExist:
        return False

@login_required(login_url='Login')
def index_roles(request):
    if verificar_permiso(request, 1):
        rol = Rol.objects.all()
        context = {'roles':rol}
        return render(request, 'rol/index_rol.html', context)
    else:
        return render(request, '403.html')
@login_required(login_url='Login')
def create_rol(request):
#En acceso se obtienen todos los permisos/accesos que se tienen en el rol especificado
#Luego se serializa en JSON y se envia más abajo en el diccionario
    if request.method == 'POST':
        form = rol_form(request.POST)
        if form.is_valid():
            form.save()
            obj = Rol.objects.latest('id')
        return render(request, 'rol/form_acceso.html', {'my_data':'{}','id_rol': obj.id})
    else:
        form = rol_form()
        return render(request, 'rol/form_rol.html', {'form':form})
@login_required(login_url='Login')
def edit_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
    if request.method == 'GET':
        form = rol_form(instance = rol)
        return render(request, 'rol/form_rol.html', {'form':form})
    else:
        obj = Rol.objects.latest('id')
        acceso = RolOpcion.objects.filter(idRol = obj.id)
        js_data = serializers.serialize('json', acceso)
        form = rol_form(request.POST, instance = rol)
        if form.is_valid():
            form.save()
        return render(request, 'rol/form_acceso.html', {'my_data':js_data, 'id_rol': obj.id})
@login_required(login_url='Login')
def create_acceso(request):
    if request.method == 'GET':
        return render(request, 'rol/form_acceso.html')

    if request.method == 'POST':
        if 'id' in request.POST:
            if 'estado' in request.POST:
                contador = 1
                for sw in switches:
                    if request.POST['id'] == sw:
                        try:
                            obj = RolOpcion.objects.filter(idRol = 1, idOpcion = contador)
                            if request.POST['estado'] == 'unchecked':
                                obj.delete()
                            if request.POST['estado'] == 'checked':
                                with connection.cursor() as cursor:
                                    cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID,IDROL_ID) VALUES ( %s , %s );", [contador,1])
                                    cursor.close()
                        except:
                            obj = RolOpcion.objects.filter(idRol = 1, idOpcion = contador)
                            if request.POST['estado'] == 'unchecked':
                                obj.delete()
                        return HttpResponse('success')
                    contador +=1

#Esta vista se encarga de recibir a traves de un POST la informacion del formulario de acceso
@login_required(login_url='Login')
def edit_acceso(request):
    if request.method == 'POST':
       if 'id' in request.POST:
           if 'estado' in request.POST:
               if 'id_rol' in request.POST:
                   identificador = request.POST['id_rol']
                   contador = 1
                   for sw in switches:
                       if request.POST['id'] == sw:
                           try:
                               obj = RolOpcion.objects.filter(idRol = identificador, idOpcion = contador)
                               if request.POST['estado'] == 'unchecked':
                                   obj.delete()
                               if request.POST['estado'] == 'checked':
                                   with connection.cursor() as cursor:
                                       cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID,IDROL_ID) VALUES ( %s , %s );", [contador,identificador])
                                       cursor.close()
                           except:
                               obj = RolOpcion.objects.filter(idRol = identificador, idOpcion = contador)
                               if request.POST['estado'] == 'unchecked':
                                   obj.delete()
                           return HttpResponse('success')
                       contador +=1
                   return redirect('index roles')

@login_required(login_url='Login')
def delete_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
    if request.method == 'POST':
        RolOpcion.objects.filter(idRol = id_rol).delete()
        rol.delete()
        return redirect('index roles')
    return render(request, 'rol/delete_rol.html', {'rol':rol})
