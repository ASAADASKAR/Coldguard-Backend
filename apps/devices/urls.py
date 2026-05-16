from django.urls import path
from .views import CustomerAPIView, DeviceAPIView

urlpatterns = [
    path('customers/', CustomerAPIView.as_view(), name='customers'),
    path('devices/', DeviceAPIView.as_view(), name='devices'),
]