"""
Dashboard URL configuration.
All endpoints are read-only GET.
"""

from django.urls import path
from .dashboard_views import (
    CurrentTemperatureView,
    TemperatureHistoryView,
    AlarmListView,
)

urlpatterns = [
    path('dashboard/current/', CurrentTemperatureView.as_view(), name='dashboard-current'),
    path('dashboard/history/', TemperatureHistoryView.as_view(), name='dashboard-history'),
    path('dashboard/alarms/', AlarmListView.as_view(), name='dashboard-alarms'),
]
