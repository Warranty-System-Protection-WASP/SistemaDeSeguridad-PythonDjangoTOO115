from django.urls import path, re_path

from apps.Rol.views import index_roles, view_rol, edit_rol, delete_rol

urlpatterns = [
    path(r'^$', index_roles, name='index roles'),
    path(r'^Nuevo$', view_rol, name='view roles'),
    path(r'^Editar/(?P<id_rol>[^/]+)/$', edit_rol, name='edit roles'),
    path(r'^Eliminar/(?P<id_rol>[^/]+)/$', delete_rol, name='delete roles'),
]
