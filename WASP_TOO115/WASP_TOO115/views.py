from django.shortcuts import render
from django.core import serializers

from apps.Rol.models import RolUsuario, RolOpcion
from apps.Cuenta.models import Usuario

import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        usuario = Usuario.objects.filter(nomUsuario = request.user)
        #rol = RolUsuario.objects.filter(idEmpleado = usuario)
        #js_data = "{}"
        js_data = serializers.serialize('json', usuario)
        '''for item in rol:
            opciones = RolOpcion.objects.filter(idRol = item)
            js_data = serializers.serialize('json', opciones)
            #return render(request, 'index.html', {'my_data':js_data})'''
        return render(request, 'index.html', {'my_data':js_data})
    else:
        return render(request, 'index.html')
