from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Imagen(models.Model):
    img_id=models.AutoField(primary_key=True)
    img_ruta = models.ImageField(upload_to='mamas', blank=True)
    img_descripcion=models.TextField()
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
