from django import forms
from .models import Device, Route
from icon.models import Marker

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('name',)

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre del Dispositivo'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('name',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Nombre del Recorrido'}),
        }