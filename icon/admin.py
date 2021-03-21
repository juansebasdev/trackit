from django.contrib import admin
from .models import Marker
# Register your models here.
class MarkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']

admin.site.register(Marker, MarkerAdmin)