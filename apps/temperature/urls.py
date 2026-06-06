from django.urls import path
from .views import TemperatureAPIView, DeviceLogAPIView

urlpatterns = [
    path('temperature/', TemperatureAPIView.as_view(), name='temperature'),
    path('logs/', DeviceLogAPIView.as_view(), name='device-logs'),
]