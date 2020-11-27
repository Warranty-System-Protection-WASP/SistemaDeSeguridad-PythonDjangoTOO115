from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

from apps.Rol.models import Rol, RolOpcion
from apps.Rol.forms import rol_form

import json

# Create your views here.

switches = ["customSwitch1","customSwitch2","customSwitch3","customSwitch4","customSwitch5","customSwitch6","customSwitch7","customSwitch8","customSwitch9","customSwitch10","customSwitch11","customSwitch12"]

def index_roles(request):
    rol = Rol.objects.all()
    context = {'roles':rol}
    return render(request, 'rol/index_rol.html', context)

def view_rol(request):
    js_data = ""
    if request.method == 'POST':
        form = rol_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index roles')
    else:
        form = rol_form()
    return render(request, 'rol/form_rol.html', {'form':form, 'my_data':js_data})

def edit_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
    #En acceso se obtienen todos los permisos/accesos que se tienen en el rol especificado
    #Luego se serializa en JSON y se envia más abajo en el diccionario
    acceso = RolOpcion.objects.filter(idRol = id_rol)
    js_data = serializers.serialize('json', acceso)
    if request.method == 'GET':
        form = rol_form(instance = rol)
    else:
        form = rol_form(request.POST, instance = rol)
        if form.is_valid():
            form.save()
        return redirect('index roles')
    return render(request, 'rol/form_rol.html', {'form':form, 'my_data':js_data})

#Esta vista se encarga de recibir a traves de un POST la informacion del formulario de acceso
def update_acceso(request):
   if request.method == 'POST':
       if 'id' in request.POST:
           if 'estado' in request.POST:
               contador = 1
               for sw in switches:
                   if request.POST['id'] == sw:
                       try:
                           if request.POST['estado'] == 'checked':
                               with connection.cursor() as cursor:
                                   cursor.execute("INSERT INTO ROL_ROLOPCION (IDOPCION_ID,IDROL_ID) VALUES ( %s , %s );", [contador,1])
                                   cursor.close()
                       except:
                           obj = RolOpcion.objects.filter(idRol = 1, idOpcion = contador)
                           #obj = obj1.filter(idOpcion = contador)
                           if request.POST['estado'] == 'unchecked':
                               obj.delete()
                               #opcion = OpcionCrud.objects.get(id = contador)
                               #rol = Rol.objects.get(id = 1)
                               #op = RolOpcion.objects.create(idOpcion = opcion, idRol = rol)
                       #if obj is None:
                        #   if request.POST['estado'] == 'checked':
                        #       op = RolOpcion.objects.create(idOpcion = contador, idRol = '1')
                               #op.save(force_insert=True)
                       #else:
                        #   if request.POST['estado'] == 'unchecked':
                        #       obj.delete()
                       return HttpResponse('success')
                   contador +=1


def delete_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
    if request.method == 'POST':
        rol.delete()
        return redirect('index roles')
    return render(request, 'rol/delete_rol.html', {'rol':rol})
