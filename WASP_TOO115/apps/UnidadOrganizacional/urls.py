#Urls para UnidadOrganizacional
from django.urls import path, re_path

#from apps.UnidadOrganizacional.views import index_unidad, delete_unidad, edit_unidad, view_unidad
from apps.UnidadOrganizacional.views import UnidadList, UnidadCreate, UnidadUpdate, UnidadDelete

urlpatterns = [

    path('', UnidadList, name='index unidad'),
    path('Agregar', UnidadCreate, name='view unidad'),
    path('Editar/<int:pk>/',UnidadUpdate, name='edit unidad'),
    path('Eliminar/<int:id_unidad>/', UnidadDelete, name='delete unidad'),
]
