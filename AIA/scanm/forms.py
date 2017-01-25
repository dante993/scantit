from models import *
from django import forms
from django.forms import Form, CharField, TextInput

class LoginForm(Form):
    cedula = CharField(max_length=10, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "placeholder": "cedula...",
                                                           "autofocus": True}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "type": "password",
                                                           "placeholder": "password..."}))

class ImagenForm(forms.ModelForm):
    img_id=models.AutoField(primary_key=True)
    img_ruta = models.ImageField(upload_to='mamas')
    img_descripcion=models.TextField()
    ESTADO_CHOICES =((u'analizada',u'Analizada'),
                    (u'no analizada',u'No Analizada'),)
    img_estado = models.CharField(max_length = 25,choices=ESTADO_CHOICES, blank=True)
    VALIDEZ_CHOICES =((u'valida',u'Valida'),
                    (u'no valida',u'No Valida'),)
    img_validez = models.CharField(max_length = 25,choices=VALIDEZ_CHOICES, blank=True)
    img_fecha=models.DateField(auto_now_add=True)
    hc_id=models.ForeignKey(Historial_clinico,verbose_name="Historial_clinico")
    class Meta:
        model = Imagen
        widgets={
            'img_ruta':forms.FileInput(attrs={
                'class':'form-control'
            }),
            'img_descripcion':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Breve descripcion del producto...'
            }),
            'img_fecha':forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'hc_id':forms.Select(attrs={
                'class':'form-control'
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
