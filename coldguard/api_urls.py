from django.urls import path, include

urlpatterns = [
    path('', include('apps.temperature.urls')),
    path('', include('apps.temperature.dashboard_urls')),
    path('', include('apps.devices.urls')),
    path('', include('apps.customers.urls')),
]