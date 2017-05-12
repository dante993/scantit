from scanm.models import *
from django import forms
from django.forms import Form, CharField, TextInput
from django.contrib.auth import authenticate

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

# ------------------------------- editar clave -----------------------------
class EditarContrasenaForm(forms.Form):
    user = forms.CharField(
        label='usuario',
        widget=forms.TextInput(attrs={'class': 'hidden'}))
    actual_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repeat the new password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        user = self.cleaned_data['user']
        actual_password = self.cleaned_data['actual_password']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        user = authenticate(username=self.cleaned_data['user'],
                            password=self.cleaned_data['actual_password'])
        if user is not None and user.is_active:
            if password != password2:
                raise forms.ValidationError('New passwords do not match.')
        else:
            raise forms.ValidationError('The current password is incorrect.')

        return password2
# ----------------------------------------------------------usuario----------------------------------------------------
class Usuario_edtForm(forms.ModelForm):
    class Meta:
        model = Usuario
        widgets={
            'nombres':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'apellidos':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'e_mail':forms.EmailInput(attrs={
                'class':'form-control'
            }),
            'telefono':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'direccion':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'sexo':forms.Select(attrs={
                'class':'form-control'
            }),
            'fecha_de_nacimiento':forms.TextInput(attrs={
                'class':'form-control datepicker',
                'type':'text',
                'value':'2016-10-10'
            }),
        }
        fields = ('nombres','apellidos','e_mail','telefono','direccion','sexo','fecha_de_nacimiento',)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        widgets={
            'cedula':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'password':forms.TextInput(attrs={
                'class':'form-control',
                'type':'password'
            }),
            'nombres':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'apellidos':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'e_mail':forms.EmailInput(attrs={
                'class':'form-control'
            }),
            'telefono':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'direccion':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'sexo':forms.Select(attrs={
                'class':'form-control'
            }),
            'fecha_de_nacimiento':forms.TextInput(attrs={
                'class':'form-control datepicker',
                'type':'text',
                'value':'2016-10-10'
            }),
        }
        fields = ('cedula','nombres','apellidos','e_mail','telefono','direccion','sexo','fecha_de_nacimiento',)

# ---------------------------------------imagenes subidas por usuarios--------------------------------------------------------
class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        widgets={
            'img_ruta':forms.FileInput(attrs={
                'accept':'image/jpg,image/png,image/jepg,image/gif,image/bmp'
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
            'hc_cedula':forms.Select(attrs={
                'class':'selectpicker',
                'data-style':'btn btn-rose btn-round'
            })
        }
        fields = '__all__'

# ---------------------------------------Historial clinico--------------------------------------------------------
class Historial_clinicoForm(forms.ModelForm):
    class Meta:
        model = Historial_clinico
        widgets={
            'hc_cedula':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'hc_nombre':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'hc_apellido':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'hc_edad':forms.NumberInput(attrs={
                'class':'form-control'
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
                'accept':'image/jpg,image/png,image/jepg,image/gif'
            }),
            'imgad_descripcion':forms.Textarea(attrs={
                'class':'form-control',
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
                'class':'selectpicker',
                'data-style':'btn btn-rose btn-round'
            }),
        }
        fields = '__all__'
