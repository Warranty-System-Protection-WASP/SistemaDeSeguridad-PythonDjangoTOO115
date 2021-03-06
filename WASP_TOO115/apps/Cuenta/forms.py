from django import forms
from django.contrib.auth.forms import PasswordChangeForm
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
    passcode = forms.CharField(label='Passcode', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '4'}))
    telefono = forms.CharField(label='Teléfono', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '8'}))
    dui = forms.CharField(label='Dui', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '9'}))
    nit = forms.CharField(label='Nit', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '14'}))
    isss = forms.CharField(label='ISSS', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '9'}))
    nup = forms.CharField(label='NUP', widget=forms.TextInput(attrs={'class': 'form-control',
    'pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '12'}))
    numCasa = forms.CharField(label='Número de casa', widget=forms.TextInput(attrs={'class': 'form-control',
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
            'genero':forms.Select(attrs={'class':'form-control'}),
            'estadoCivil':forms.Select(attrs={'class':'form-control'}),
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
            'salario': forms.TextInput(attrs={'class':'form-control', 'pattern': '[0-9, "."]+', 'title':'Sólo números'}),            
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

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Contraseña actual'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nueva Contraseña'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmación de nueva contraseña'

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Ingrese una nueva contraseña',
    'class': 'form-control',
    'autocomplete': 'off'}))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Repita la nueva contraseña',
    'class': 'form-control',
    'autocomplete': 'off'}))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cleaned
