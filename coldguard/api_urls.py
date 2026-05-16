from django.urls import path, include

urlpatterns = [
    path('', include('apps.temperature.urls')),
    path('', include('apps.devices.urls')),
]