from django.db import models


class Customer(models.Model):
    """
    Represents a ColdGuard customer.
    One customer can have multiple devices.
    """
    name       = models.CharField(max_length=200)
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.name} ({self.email})"


class Device(models.Model):
    """
    Represents a ColdGuard ESP32 device.
    Each device belongs to one customer.
    """
    customer   = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    device_key = models.CharField(max_length=100, unique=True)
    name       = models.CharField(max_length=200)
    location   = models.CharField(max_length=200, blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f"{self.name} — {self.customer.name}"