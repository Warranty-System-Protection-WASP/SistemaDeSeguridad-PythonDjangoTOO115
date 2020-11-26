"""WASP_TOO115 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from WASP_TOO115.views import index
from apps.Cuenta import views

from apps.Rol.views import index_roles, view_rol, edit_rol, delete_rol

#Librerias para el login
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path(r'^Roles$', index_roles, name='index roles'),
    path(r'^Roles/Nuevo$', view_rol, name='view roles'),
    path(r'^Roles/Editar/(?P<id_rol>[^/]+)/$', edit_rol, name='edit roles'),
    path(r'^Roles/Eliminar/(?P<id_rol>[^/]+)/$', delete_rol, name='delete roles'),
    #path('prueba/', views.index),
    #Url para el login
    #path('login/', LoginView.as_view(template_name='login/login.html'), name='login'),
]
