from django.db import models


class TemperatureReading(models.Model):
    """
    Stores a single temperature reading from an ESP32 device.
    Created every time the device sends data to the API.
    """

    # Device identifier — matches DEVICE_KEY in firmware
    device_key = models.CharField(max_length=100)

    # Temperature value in Celsius
    temperature = models.FloatField()

    # Status: OK, ALARM_HIGH, ALARM_LOW
    status = models.CharField(max_length=20)

    # Automatically set when reading is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first
        verbose_name = 'Temperature Reading'
        verbose_name_plural = 'Temperature Readings'

    def __str__(self):
        return f"{self.device_key} — {self.temperature}°C ({self.status})"