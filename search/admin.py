from django.contrib import admin
from .models import Device, Coordinate, Route
# Register your models here.
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('device', 'longitude', 'latitude', 'update')
    ordering = ['-update',]
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'device', 'created', 'update')
    ordering = ['-created']
admin.site.register(Coordinate, CoordinateAdmin)
admin.site.register(Device)
admin.site.register(Route, RouteAdmin)