from django.urls import path
from .views import DeviceAPIView

urlpatterns = [
    path('devices/', DeviceAPIView.as_view(), name='devices'),
]