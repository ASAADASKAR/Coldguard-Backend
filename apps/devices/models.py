from django.db import models
from apps.customers.models import Customer  # ← import von customers app


class Device(models.Model):
    """
    Represents a ColdGuard ESP32 device.
    Each device belongs to one customer.
    """
    customer     = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    device_key   = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    location     = models.CharField(max_length=200, blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f"{self.display_name} — {self.customer.name}"