from django.urls import path
from .views import TemperatureAPIView

urlpatterns = [
    path('temperature/', TemperatureAPIView.as_view(), name='temperature'),
]