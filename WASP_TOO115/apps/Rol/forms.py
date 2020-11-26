from django import forms

from apps.Rol.models import Rol

class rol_form(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'nombreRol',
            'descripRol',
        ]
        labels = {
            'nombreRol':'Título',
            'descripRol':'Descripción',
        }
        widgets = {
            'nombreRol':forms.TextInput(attrs={'class':'form-control'}),
            'descripRol':forms.TextInput(attrs={'class':'form-control'}),
        }
