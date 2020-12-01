#Urls para UnidadOrganizacional
from django.urls import path, re_path

from apps.UnidadOrganizacional.views import index_unidad, delete_unidad, edit_unidad, view_unidad

urlpatterns = [
    path('',index_unidad, name="index unidad"),
    path('Agregar',view_unidad, name='view unidad'),
    path('Editar/(?P<id_unidad>[^/]+)/',edit_unidad, name='edit unidad'),
    path('Eliminar/(?P<id_unidad>[^/]+)/',delete_unidad, name='delete unidad'),
]