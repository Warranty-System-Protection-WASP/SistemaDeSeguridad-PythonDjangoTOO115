from django import forms

from apps.Rol.models import Rol

class rol_form(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'nombreRol',
            'descripRol',
            'unidad',
        ]
        labels = {
            'nombreRol':'Título',
            'descripRol':'Descripción',
            'unidad':'Unidad/Departamento',
        }
        widgets = {
            'nombreRol':forms.TextInput(attrs={'class':'form-control'}),
            'descripRol':forms.TextInput(attrs={'class':'form-control'}),
            'unidad':forms.Select(attrs={'class': 'form-control'}),
        }
