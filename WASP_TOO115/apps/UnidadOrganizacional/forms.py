from django import forms

from apps.UnidadOrganizacional.models import UnidadOrganizacional

#Formulario para las unidades organizacionales con los campos requeridos para llenarla 
class unidad_form(forms.ModelForm):
    class Meta:
        model=UnidadOrganizacional

        fields=[
            'idUnidad',
            'idRol',
            'nombreUnidad',
            'descripUnidad',
        ]

        labels={
            'idRol': 'Rol',
            'nombreUnidad': 'Titulo',
            'descripUnidad': 'Descripción',
        }

        widgets={            
            'idRol': forms.CheckboxSelectMultiple(),
            'nombreUnidad':forms.TextInput(attrs={'class':'form-control'}),
            'descripUnidad':forms.TextInput(attrs={'class':'form-control'}),
        }
