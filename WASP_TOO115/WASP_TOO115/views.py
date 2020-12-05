from django.shortcuts import render
from django.core import serializers

from apps.Rol.models import RolUsuario, RolOpcion, Rol
from apps.Cuenta.models import Usuario

import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(nomUsuario = request.user)
        roluser = RolUsuario.objects.get(idEmpleado = usuario, is_activo=True)
        puesto = Rol.objects.get(id = roluser.idRol.id)
        opciones = RolOpcion.objects.filter(idRol = puesto)
        #js_data = "{}"
        acceso = serializers.serialize('json', opciones)
        return render(request, 'index.html', {'permisos':acceso})
    else:
        return render(request, 'index.html')
