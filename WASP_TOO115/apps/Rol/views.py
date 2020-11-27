from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core import serializers
from apps.Rol.models import Rol, RolOpcion
from apps.Rol.forms import rol_form

import json

# Create your views here.
def index_roles(request):
    rol = Rol.objects.all()
    context = {'roles':rol}
    return render(request, 'rol/index_rol.html', context)

def view_rol(request):
    if request.method == 'POST':
        form = rol_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index roles')
    else:
        form = rol_form()
    return render(request, 'rol/form_rol.html', {'form':form})

def edit_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
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

def delete_rol(request, id_rol):
    rol = Rol.objects.get(id = id_rol)
    if request.method == 'POST':
        rol.delete()
        return redirect('index roles')
    return render(request, 'rol/delete_rol.html', {'rol':rol})
