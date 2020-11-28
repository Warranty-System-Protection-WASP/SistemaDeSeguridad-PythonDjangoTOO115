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
from django.urls import path, re_path
from django.conf.urls import include
from WASP_TOO115.views import index
from apps.Cuenta import views
from django.contrib.auth.decorators import login_required
from apps.Cuenta.views import Login, Logout

from apps.Rol.views import index_roles, view_rol, edit_rol, delete_rol

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path(r'^Roles$', include('apps.Rol.urls'), name='roles'),
    path('Cuenta/', include('apps.Cuenta.urls', namespace='Cuenta')),
    path('accounts/login/', Login.as_view(), name = 'Login'),
    path('logout', login_required(Logout), name = 'Logout'),
]
