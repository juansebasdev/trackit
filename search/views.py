from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from .models import Device, Coordinate, Route
from icon.models import Marker
from .forms import DeviceForm, RouteForm
# Create your views here.

@method_decorator(login_required, name='dispatch')
class RouteDelete(DeleteView):
    model = Route
    success_url = reverse_lazy('search:route_list')

@method_decorator(login_required, name='dispatch')
class RouteFormView(FormView):
    form_class = RouteForm
    template_name = 'search/route_form.html'
    success_url = reverse_lazy('search:route_list')

    def get_success_url(self):
        return reverse_lazy('search:route_list') + '?started'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = Device.objects.filter(profile=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            route_name = request.POST.get("name")
            device_id = request.POST.get("device")
            device = Device.objects.get(id=device_id)
            new_route = Route.objects.create(name=route_name, device=device)
            new_route.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class RouteListView(ListView):
    model = Route
    template_name = 'search/route_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for route in context['route_list']:
            if route.device.profile != self.request.user.profile:
                context['route_list'] = context['route_list'].exclude(name=route.name)
            if route.activate:
                context['activate'] = True
        return context

@method_decorator(login_required, name='dispatch')
class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('search:device_list')

@method_decorator(login_required, name='dispatch')
class DeviceUpdateView(UpdateView):
    form_class = DeviceForm
    template_name = 'search/device_form.html'
    #success_url = reverse_lazy('device_list')

    def get_success_url(self):
        return reverse_lazy('search:device_list') + '?update'

    def get_object(self):
        device_id = self.kwargs['pk']
        device, created = Device.objects.get_or_create(id=device_id)
        return device

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = Marker.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        marker_color = request.POST.get('marker')
        device_name = request.POST.get('name')
        device = Device.objects.get(profile=request.user.profile, name=device_name)
        device.marker = Marker.objects.get(color=marker_color)
        device.save()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class DeviceFormView(FormView):
    form_class = DeviceForm
    template_name = 'search/device_form.html'
    #success_url = reverse_lazy('device_list')

    def get_success_url(self):
        return reverse_lazy('search:device_list') +'?register'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        name_device = request.POST.get('name')
        marker_color = request.POST.get('marker')

        if form.is_valid():
            marker = Marker.objects.get(color=marker_color)
            new_device = Device.objects.create(profile=request.user.profile, name=name_device, marker=marker)
            new_device.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = Marker.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class DeviceListView(ListView):
    model = Device
    template_name = 'search/device_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_list'] = Device.objects.filter(profile=self.request.user.profile)
        return context

@method_decorator(login_required, name='dispatch')
class MapView(TemplateView):
    template_name = 'search/root_map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['devices'] = Device.objects.filter(profile=self.request.user.profile)
        return context

def device_coordinate(request):
    json_response = {'created':False}
    if request.user.is_authenticated:
        value = request.GET.get("dev", None)
        json_response['routes'] = []
        if value == "all":
            devices = Device.objects.filter(profile=request.user.profile)
            json_response['created'] = True
            json_response['all'] = True
            json_response['location'] = []
            for i in range(0, len(devices)):
                coordinate = Coordinate.objects.filter(device=devices[i]).last()
                routes = Route.objects.filter(device=devices[i])
                if coordinate:
                    json_response['location'].append({'device':devices[i].name, 'lat':coordinate.latitude, 'long':coordinate.longitude, 'icon':coordinate.device.marker.image.url})
                if routes:
                    for route in routes:
                        json_response['routes'].append({'name':route.name, 'value':route.id})
            if len(json_response['location']) == 0:
                 json_response['location'] = False
            if len(json_response['routes']) == 0:
                json_response['routes'] = False
        else:
            device = Device.objects.get(id=value)
            coordinate = Coordinate.objects.filter(device=device).last()
            routes = Route.objects.filter(device=device)
            if coordinate:
                json_response['created'] = True
                json_response['name'] = coordinate.device.name
                json_response['icon'] = coordinate.device.marker.image.url
                json_response['long'] = coordinate.longitude
                json_response['lat'] = coordinate.latitude
            if routes:
                for route in routes:
                    json_response['routes'].append({'name':route.name, 'value':route.id})
            if len(json_response['routes']) == 0:
                json_response['routes'] = False
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def device_route(request):
    json_response = {'created':False}
    if request.user.is_authenticated:
        value = request.GET.get("rt", None)
        route = Route.objects.get(id=value)
        if route:
            json_response['created'] = True
            json_response['coordinates'] = []
            coordinates = []
            for coordinate in route.coordinate.all():
                    coordinates.append([coordinate.latitude, coordinate.longitude])
                    #print(coordinates)
            json_response['coordinates'] = coordinates
            json_response['route'] = {'name':route.name, 'device':route.device.name, 'activate':route.activate}
            #print(json_response['route'])
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

def route_stop(request):
    if request.user.is_authenticated:
        value = request.GET.get("id", None)
        if value:
            route = Route.objects.get(id=value)
            route.activate = False
            route.save()
    else:
        raise Http404("User is not authenticated")
    return render(request, 'search/route_list.html')

def is_route(request):
    json_response = {'created':'False'}
    if request.user.is_authenticated:
        dev = request.GET.get("val", None)
        if dev:
            json_response['created'] = True
            device = Device.objects.get(id=dev)
            routes = Route.objects.filter(device=device)
            if routes:
                for route in routes:
                    if route.activate == True:
                        json_response['activated'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)