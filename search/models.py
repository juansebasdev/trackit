from django.db import models
from registration.models import Profile
from icon.models import Marker

from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Device(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Nombre dispositivo') 
    marker = models.ForeignKey(Marker, on_delete=models.PROTECT ,verbose_name='Icono', null=True, blank=True)

    class Meta:
        verbose_name = 'dispositivo'
        verbose_name_plural = 'dispositivos'

    def __str__(self):
        return self.name

class Coordinate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Dispositivo')
    latitude = models.DecimalField(verbose_name='Latitud', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(verbose_name='Longitud', max_digits=9, decimal_places=6)
    update = models.DateTimeField(auto_now_add=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'coordenada'
        verbose_name_plural = 'coordenadas'
        ordering = ['update',]

    def __str__(self):
        return self.device.name

class Route(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre Ruta")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
    coordinate = models.ManyToManyField(Coordinate)
    activate = models.BooleanField(verbose_name='Activo', default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    update = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = "recorrido"
        verbose_name_plural = "recorridos"
        ordering = ['created',]

    def __str__(self):
        return self.name

@receiver(post_save, sender=Coordinate)
def coordinate_in_route(sender, instance, **kwargs):
    device = Device.objects.get(name=instance)
    try:
        route = Route.objects.get(device=device, activate=True)
        route.coordinate.add(instance)
        route.save()
    except Exception:
        pass
