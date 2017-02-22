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

# ----------------------------------------------------------usuario----------------------------------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        widgets={
            'cedula':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba su cedula...'
            }),
            'password':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba su clave...',
                'type':'password'
            }),
            'nombres':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba sus nombres...'
            }),
            'apellidos':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba sus apellidos...'
            }),
            'e_mail':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba su correo...'
            }),
            'telefono':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba su telefono...'
            }),
            'direccion':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Escriba su direccion...'
            }),
            'sexo':forms.Select(attrs={
                'class':'form-control'
            }),
            'fecha_de_nacimiento':forms.TextInput(attrs={
                'class':'datepicker form-control',
                'type':'text',
                'readonly':'',
                'data-date-format':'yyyy-mm-dd',
                'value':'Fecha de nacimiento...'
            }),
        }
        fields = ('cedula','nombres','apellidos','e_mail','telefono','direccion','sexo','fecha_de_nacimiento',)

# ---------------------------------------imagenes subidas por usuarios--------------------------------------------------------
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
                'class':'form-control'
            }),
            'img_validez':forms.Select(attrs={
                'class':'datepicker form-control'
            }),
            'img_fecha':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'hc_cedula':forms.Select(attrs={
                'class':'datepicker form-control'
            })
        }
        fields = '__all__'

# ---------------------------------------Historial clinico--------------------------------------------------------
class Historial_clinicoForm(forms.ModelForm):
    class Meta:
        model = Historial_clinico
        widgets={
            'hc_cedula':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del paciente...'
            }),
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

# ---------------------------------------tipos de cancer--------------------------------------------------------
class Tipo_cancerForm(forms.ModelForm):
    class Meta:
        model = Tipo_cancer
        widgets={
            'tc_nombre':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del tipo de cancer...'
            }),
            'tc_descripcion':forms.Textarea(attrs={
                'class':'form-control',
            }),
            'tc_estado':forms.Select(attrs={
                'class':'form-control'
            })
        }
        fields = '__all__'

# ---------------------------------------imagenes para aprendizaje--------------------------------------------------------
class Imagen_admForm(forms.ModelForm):
    class Meta:
        model = Imagen_adm
        widgets={
            'imgad_ruta':forms.FileInput(attrs={
                'class':'form-control',
                'accept':'image/jpg,image/png,image/jepg,image/gif'
            }),
            'imgad_descripcion':forms.Textarea(attrs={
                'class':'form-control',
            }),
            'imgad_fecha':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'imgad_ancho':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'ancho...'
            }),
            'imgad_alto':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'alto...'
            }),
            'imgad_estado':forms.Select(attrs={
                'class':'form-control'
            }),
            'tc_id':forms.Select(attrs={
                'class':'form-control'
            }),
        }
        fields = '__all__'
