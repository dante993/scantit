from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.
# ..........................................................

class UserManager(BaseUserManager,models.Manager):
    def _create_user(self,cedula,nombres,apellidos,e_mail,password,is_staff,
                    is_superuser,**extra_fields):
        e_mail=self.normalize_email(e_mail)
        if not e_mail:
            raise ValueError('Debe Ingresar un e-mail Obligatoriamente!')
        user = self.model(cedula=cedula,nombres=nombres,apellidos=apellidos,e_mail=e_mail,is_staff=is_staff,
                            is_active=True,is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,cedula,nombres,apellidos,e_mail,password=None,**extra_fields):
        return self._create_user(cedula,nombres,apellidos,e_mail,password,False,False,**extra_fields)

    def create_superuser(self,cedula,nombres,apellidos,e_mail,password=None,**extra_fields):
        return self._create_user(cedula,nombres,apellidos,e_mail,password,True,True,**extra_fields)

def validar_cedula(value):
        ced_cliente=value
        msg = "La Cedula introducida no es valida"
        if ced_cliente.isdigit():
            cant_num_cedula=len(ced_cliente.split()[0])
            msg = "La Cedula introducida no es valida"
            if cant_num_cedula == 10 :
                valores = [ int(ced_cliente[x]) * (2 - x % 2) for x in range(9) ]
                suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
                veri = 10 - (suma - (10 * (suma / 10)))
                if int(ced_cliente[9]) == int(str(veri)[-1:]):
                    return ced_cliente
                else:
                    raise forms.ValidationError(msg)
            else:raise forms.ValidationError(msg)
        else:raise forms.ValidationError("esto no es un numero de cedula")

class Usuario (AbstractBaseUser,PermissionsMixin):
    cedula = models.CharField(primary_key=True,max_length = 10,validators=[validar_cedula])
    nombres = models.CharField(max_length = 50)
    apellidos = models.CharField(max_length = 50)
    e_mail = models.EmailField()
    telefono = models.CharField(max_length = 25)
    direccion=models.CharField(max_length = 200)
    SEXO_CHOICES = (
        (u'm', u'Malculino'),
        (u'f', u'Femenino'),
    )
    sexo=models.CharField(max_length = 2,choices=SEXO_CHOICES)
    fecha_de_nacimiento=models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    object=UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['e_mail','nombres','apellidos']
    def __unicode__(self):
        strgn=self.cedula
        return strgn
admin.site.register(Usuario)

# ..........................................................

class Historial_clinico(models.Model):
    hc_id=models.AutoField(primary_key=True)
    hc_nombre = models.CharField(max_length = 25,verbose_name="Nombre")
    hc_apellido = models.CharField(max_length = 25,verbose_name="Apellido")
    hc_edad = models.IntegerField(verbose_name="Edad")
    hc_fecha = models.DateField(auto_now_add = True,verbose_name="Fecha")
    ESTADO_CHOICES =((u'activo',u'Activo'),
                    (u'inactivo',u'Inactivo'),)
    hc_estado = models.CharField(max_length = 25,choices=ESTADO_CHOICES,verbose_name="Estado", default='activo',blank=True)
    cedula=models.ForeignKey(Usuario,verbose_name="Usuario")
    def __unicode__(self):
        strgn=self.hc_nombre+' '+self.hc_apellido
        return strgn

class Imagen(models.Model):
    img_id=models.AutoField(primary_key=True)
    img_ruta = models.ImageField(upload_to='mamas')
    img_descripcion=models.TextField()
    ESTADO_CHOICES =((u'analizada',u'Analizada'),
                    (u'no analizada',u'No Analizada'),)
    img_estado = models.CharField(max_length = 25,choices=ESTADO_CHOICES, default='no analizada')
    VALIDEZ_CHOICES =((u'valida',u'Valida'),
                    (u'no valida',u'No Valida'),)
    img_validez = models.CharField(max_length = 25,choices=VALIDEZ_CHOICES, default='valida')
    img_fecha=models.DateField(auto_now_add=True)
    hc_id=models.ForeignKey(Historial_clinico,verbose_name="Historial_clinico")
    def __unicode__(self):
        return self.img_ruta

class Area_imagen(models.Model):
    arim_id=models.AutoField(primary_key=True)
    arim_pos_x = models.DecimalField(max_digits=19, decimal_places=3)
    arim_pos_y = models.DecimalField(max_digits=19, decimal_places=3)
    arim_ancho = models.DecimalField(max_digits=19, decimal_places=3)
    arim_alto = models.DecimalField(max_digits=19, decimal_places=3)
    img_id=models.ForeignKey(Imagen,verbose_name="imagen")
    def __unicode__(self):
        return self.arim_id

class Tipo_cancer(models.Model):
    tc_id = models.AutoField(primary_key=True)
    tc_nombre = models.CharField(max_length = 25)
    tc_descripcion=models.TextField()
    ESTADO_CHOICES =((u'activo',u'Activo'),
                    (u'inactivo',u'Inactivo'),)
    tc_estado = models.CharField(max_length = 25,choices=ESTADO_CHOICES, default='activo')
    def __unicode__(self):
        return self.tc_nombre


class Resultados_analisis(models.Model):
    resan_id=models.AutoField(primary_key=True)
    resan_fecha=models.DateField(auto_now_add=True)
    resan_descripcion=models.TextField()
    img_id=models.ForeignKey(Imagen,verbose_name="imagen")
    tc_id=models.ForeignKey(Tipo_cancer,verbose_name="tipo_cancer")



# ........
