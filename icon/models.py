from django.db import models

# Create your models here.
class Marker(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre Icono')
    image = models.ImageField(upload_to = 'icon/', blank = True, null = True, verbose_name = 'Icono')
    color = models.CharField(max_length=7, verbose_name='Color', null=True, blank=True)

    class Meta:
        verbose_name = 'marcador'
        verbose_name_plural = 'marcadores'

    def __str__(self):
        return self.color