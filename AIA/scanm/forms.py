from models import *
from django import forms

class LoginForm(Form):
    username = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "placeholder": "Nombre de usuario",
                                                           "autofocus": True}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "type": "password",
                                                           "placeholder": "Contrasenia"}))

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        widgets={
            'img_ruta':forms.FileInput(attrs={
                'class':'form-control'
            }),
            'img_descripcion':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Breve descripcion del producto...'
            })
        }
        fields = '__all__'
