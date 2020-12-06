from django import forms
import datetime
from .models import *

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = [
        'nomDepartamento',
        ]
        labels = {
        'nomDepartamento' : 'Departamento'
        }
        widgets = {
        'nomDepartamento' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = [
        'nomMunicipio',
        'departamento',
        ]
        labels = {
        'nomMunicipio' : 'Municipio',
        'departamento' : 'Departamento',
        }
        widgets = {
        'nomMunicipio' : forms.TextInput(attrs={'class': 'form-control'}),
        'departamento' : forms.Select(attrs={'class': 'form-control'}),
        }

#Formulario para la solicitud de SignUp
class SignUpForm(forms.ModelForm):
    passcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '4'}))
    class Meta:
        model = Usuario
        #Atributos/Campos a utilizar
        fields = [
            'nombre',
            'apellido',
            'fechaNacimiento',
            'telefono',
            'dui',
            'nit',
            'isss',
            'nup',
            'genero',
            'estadoCivil',
            'numCasa',
            'calle',
            'colonia',
            'correo',
            'passcode',
        ]
        #Labels a utilizar
        labels = {
            'nombre':'Nombres',
            'apellido':'Apellidos',
            'fechaNacimiento':'Fecha de Nacimiento',
            'telefono':'Telefono',
            'dui':'DUI',
            'nit':'NIT',
            'isss':'ISSS',
            'nup':'NUP',
            'genero':'Genero',
            'estadoCivil':'Estado Civil',
            'numCasa':'Numero de Casa',
            'calle':'Calle',
            'colonia':'Colonia',
            'correo':'Correo',
            'passcode':'Passcode',
        }

        #Widgets a utilizar
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'apellido':forms.TextInput(attrs={'class':'form-control', 'name': 'ap'}),
            'fechaNacimiento':forms.DateInput(attrs={'type':'date', 'value':datetime.datetime.now().strftime('%Y-%m-%d')}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'dui':forms.TextInput(attrs={'class':'form-control'}),
            'nit':forms.TextInput(attrs={'class':'form-control'}),
            'isss':forms.TextInput(attrs={'class':'form-control'}),
            'nup':forms.TextInput(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'estadoCivil':forms.Select(attrs={'class':'form-control'}),
            'numCasa':forms.TextInput(attrs={'class':'form-control'}),
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            'correo':forms.EmailInput(attrs={'class':'form-control'}),
        }

class AprobarForm(forms.ModelForm):
    class Meta:
        model = Usuario
        #Atributos/Campos a utilizar
        fields = [
            'nombre',
            'apellido',
            'dui',
            'salario',
            'solicitud',
        ]
        #Labels a utilizar
        labels = {
            'nombre':'Nombres',
            'apellido':'Apellidos',
            'dui':'DUI',
            'salario': 'Salario',
            'solicitud':'Solicitud',
        }

        #Widgets a utilizar
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
            'apellido':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
            'dui':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
            'salario': forms.TextInput(attrs={'class':'form-control', 'pattern': '[0-9, "."]+', 'title':'Sólo números'})
        }

class usuario_form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nomUsuario',
            'nombre',
            'apellido',
            'fechaNacimiento',
            'correo',
            'telefono',
            'dui',
            'nit',
            'isss',
            'nup',
            'genero',
            'estadoCivil',
            'numCasa',
            'calle',
            'colonia',
            'municipio',
        ]
        labels = {
            'nomUsuario':'UserName',
            'nombre':'Nombre',
            'apellido':'Apellido',
            'fechaNacimiento':'Fecha De Nacimiento',
            'correo':'Correo Electrónico',
            'telefono':'#Teléfono',
            'dui':'#DUI',
            'nit':'NIT',
            'isss':'ISSS',
            'nup':'NUP',
            'salario':'Salario($)',
            'genero':'Sexo',
            'estadoCivil':'Estado Civil',
            'numCasa':'#Casa',
            'calle':'Calle',
            'colonia':'Colonia',
            'municipio':'Municipio',
        }
        widgets = {
            'nomUsuario':forms.TextInput(attrs={'class':'form-control', 'readonly':'True'}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'apellido':forms.TextInput(attrs={'class':'form-control', 'name': 'ap'}),
            'fechaNacimiento':forms.DateInput(attrs={'type':'date', 'value':datetime.datetime.now().strftime('%Y-%m-%d')}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
            'dui':forms.TextInput(attrs={'class':'form-control'}),
            'nit':forms.TextInput(attrs={'class':'form-control'}),
            'isss':forms.TextInput(attrs={'class':'form-control'}),
            'nup':forms.TextInput(attrs={'class':'form-control'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
            'estadoCivil':forms.Select(attrs={'class':'form-control'}),
            'numCasa':forms.TextInput(attrs={'class':'form-control'}),
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            'correo':forms.EmailInput(attrs={'class':'form-control'}),
            'municipio':forms.Select(attrs={'class': 'form-control'}),
        }
