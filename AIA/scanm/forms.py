from models import *
from django import forms
from django.forms import Form, CharField, TextInput

class LoginForm(Form):
    cedula = CharField(max_length=10, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "placeholder": "Cedula...",
                                                           "type": "text",
                                                           "autofocus": True}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "type": "password",
                                                           "placeholder": "Password..."}))

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        widgets={
            'img_ruta':forms.FileInput(attrs={
                'class':'form-control',
                'accept':'image/jpg,image/png,image/jepg'
            }),
            'img_descripcion':forms.Textarea(attrs={
                'class':'form-control',
            }),
            'img_estado':forms.Select(attrs={
                'class':'datepicker form-control'
            }),
            'img_validez':forms.Select(attrs={
                'class':'datepicker form-control'
            }),
            'img_fecha':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'hc_id':forms.Select(attrs={
                'class':'datepicker form-control'
            }),
        }
        fields = '__all__'

class Historial_clinicoForm(forms.ModelForm):
    class Meta:
        model = Historial_clinico
        widgets={
            'hc_nombre':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del paciente...'
            }),
            'hc_apellido':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Apellidos del paciente...'
            }),
            'hc_edad':forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Edad del paciente...'
            }),
            'hc_fecha':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'hc_estado':forms.Select(attrs={
                'class':'form-control'
            }),
            'cedula':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'cedula...'
            })
        }
        fields = '__all__'
