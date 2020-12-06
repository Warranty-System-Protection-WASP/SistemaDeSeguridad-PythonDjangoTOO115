from django.urls import path, re_path
from .views import *

app_name = 'Cuenta'

urlpatterns = [

    #URL para CRUD de Departamento
    path('CrearDepartamento', CrearDepartamento.as_view(), name = 'CrearDepartamento'),
    path('Departamento/<int:pk>', EditarDepartamento.as_view(), name = 'ModificarDepartamento'),
    path('Departamentos/<int:pk>/Borrar', EliminarDepartamento.as_view(), name = 'EliminarDepartamento'),
    path('Departamentos', AdministrarDepartamentos.as_view(), name = 'AdministrarDepartamentos'),
    #URL para CRUD de Municipio
    path('CrearMunicipio', CrearMunicipio.as_view(), name = 'CrearMunicipio'),
    path('Municipio/<int:pk>', EditarMunicipio.as_view(), name = 'ModificarMunicipio'),
    path('Municipios/<int:pk>/Borrar', EliminarMunicipio.as_view(), name = 'EliminarMunicipio'),
    path('Municipios', AdministrarMunicipios.as_view(), name = 'AdministrarMunicipios'),
    #path('Solicitudes', AdministrarSolicitudes.as_view(), name = 'Solicitudes'),
    re_path(r'^Aprobar/(?P<pk>\w+)', Aprobar.as_view(), name = 'AprobarSolicitud'),
    #Detalle usuario
    re_path(r'^DetalleUsuario/(?P<pk>\w+)', DetalleUsuario.as_view(), name = 'DetalleUsuario'),
    #Para cambiar contraseña
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    #Para Usuarios
    path('Usuarios/', index_usuarios, name='index usuarios'),
    path('Usuarios/<slug:username>', edit_usuario, name='edit usuarios'),
    path('Usuarios/<slug:username>/Bloquear', bloquear_usuario, name='block usuarios'),
    path('Usuarios/<slug:username>/Desbloquear', desbloquear_usuario, name='unblock usuarios'),
]
