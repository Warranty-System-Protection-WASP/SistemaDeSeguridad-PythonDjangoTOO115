from django.urls import path, re_path

from apps.Rol.views import index_roles, edit_rol, delete_rol, edit_acceso, create_acceso, create_rol

urlpatterns = [
    path('', index_roles, name='index roles'),
    path('Nuevo', create_rol, name='create roles'),
    path('Editar/(?P<id_rol>[^/]+)/', edit_rol, name='edit roles'),
    path('Eliminar/(?P<id_rol>[^/]+)/', delete_rol, name='delete roles'),
    path('FormAcceso/', create_acceso, name="acceso form"),
    path('UpdateAcceso', edit_acceso, name='edit acceso'),
]
