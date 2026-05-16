from django.db import models
from apps.devices.models import Device


class TemperatureReading(models.Model):
    """
    Stores a single temperature reading from an ESP32 device.
    Created every time the device sends data to the API.
    """

    # Link to Device model — replaces plain device_key string
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='readings'
    )

    # Temperature value in Celsius
    temperature = models.FloatField()

    # Status: OK, ALARM_HIGH, ALARM_LOW
    status = models.CharField(max_length=20)

    # Automatically set when reading is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Temperature Reading'
        verbose_name_plural = 'Temperature Readings'

    def __str__(self):
        return f"{self.device.name} — {self.temperature}°C ({self.status})"