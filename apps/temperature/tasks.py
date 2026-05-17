"""
ColdGuard Temperature Tasks

Background tasks for temperature monitoring.
Runs automatically via Celery Beat scheduler.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import TemperatureReading
from .notifications import NotificationService
from .constants import TemperatureStatus, HeartbeatConfig
from apps.devices.models import Device


@shared_task  
def check_heartbeat():
    """
    Checks if all active devices have sent data within
    the heartbeat timeout period.

    Runs automatically every CHECK_INTERVAL seconds via Celery Beat.

    If no signal received within TIMEOUT_MINUTES:
    - Sends alarm notification to device owner
    - Possible causes: power outage, WiFi failure, device malfunction
    """

    # Calculate timeout threshold
    timeout = timezone.now() - timedelta(
        minutes=HeartbeatConfig.TIMEOUT_MINUTES
    )

    # Get all active devices
    devices = Device.objects.filter(is_active=True)

    for device in devices:

        # Check if device has any readings at all
        if not device.readings.exists():
            continue

        # Get last reading for this device
        last_reading = device.readings.latest('created_at')

        # Check if last reading is older than timeout
        if last_reading.created_at < timeout:
            NotificationService.send_alarm(
                device_key=device.device_key,
                temperature=last_reading.temperature,
                status=TemperatureStatus.HEARTBEAT_FAILURE,
                created_at=last_reading.created_at,
                recipient_email=device.customer.email,
            )