from django.urls import path
from .views import MapView, DeviceListView, DeviceFormView, DeviceUpdateView, DeviceDelete, device_coordinate, device_route, Coordinate, RouteFormView, RouteListView, RouteDelete, route_stop, is_route, receive_coordinate

search_patterns = ([
    path('map/', MapView.as_view(), name='map'),
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/<int:pk>/', DeviceUpdateView.as_view(), name='device'),
    path('devices/delete/<int:pk>/', DeviceDelete.as_view(), name='device_delete'),
    path('devices/register/', DeviceFormView.as_view(), name='device_register'),
    path('routes/start/', RouteFormView.as_view(), name='route_start'),
    path('routes/stop/', route_stop, name='route_stop'),
    path('routes/', RouteListView.as_view(), name='route_list'),
    path('routes/delete/<int:pk>/', RouteDelete.as_view(), name='route_delete'),
    path('map/device/', device_coordinate, name='selected_device'),
    path('map/route/', device_route, name='selected_route'),
    path('routes/is_route/', is_route, name='is_route'),
    path('map/gprs/', receive_coordinate, name='receive')
], "search")