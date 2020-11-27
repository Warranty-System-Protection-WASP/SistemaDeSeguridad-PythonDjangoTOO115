from django.urls import path, re_path

from apps.Rol.views import index_roles, view_rol, edit_rol, delete_rol, update_acceso

urlpatterns = [
    path('', index_roles, name='index roles'),
    path('Nuevo', view_rol, name='view roles'),
    path('Editar/(?P<id_rol>[^/]+)/', edit_rol, name='edit roles'),
    path('Eliminar/(?P<id_rol>[^/]+)/', delete_rol, name='delete roles'),
    path('Acceso', update_acceso, name='update acceso'),
]
