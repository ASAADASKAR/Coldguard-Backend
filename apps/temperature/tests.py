from django.test import TestCase
from apps.customers.models import Customer
from apps.devices.models import Device
from apps.temperature.models import TemperatureReading


class TemperatureGETTestCase(TestCase):
    """Tests for GET /api/temperature/ endpoint."""

    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Restaurant",
            email="test@restaurant.de",
            phone="+49 40 123456"
        )
        self.device = Device.objects.create(
            customer=self.customer,
            device_key="coldguard-test-get",
            display_name="Test Fridge",
            location="Kitchen",
            is_active=True
        )
        TemperatureReading.objects.create(
            device=self.device,
            temperature=4.5,
            status="OK"
        )

    def test_get_by_device_key(self):
        """GET with device_key returns readings."""
        response = self.client.get(
            '/api/temperature/?device_key=coldguard-test-get'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_by_customer_id(self):
        """GET with customer_id returns all device readings."""
        response = self.client.get(
            f'/api/temperature/?customer_id={self.customer.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_missing_params(self):
        """GET without params returns 400."""
        response = self.client.get('/api/temperature/')
        self.assertEqual(response.status_code, 400)

    def test_get_invalid_device_key(self):
        """GET with wrong device_key returns 404."""
        response = self.client.get(
            '/api/temperature/?device_key=wrong-key'
        )
        self.assertEqual(response.status_code, 404)

    def test_get_by_customer_id_multiple_devices(self):
        """GET with customer_id returns readings from ALL devices."""
        
        # Second device for same customer
        device2 = Device.objects.create(
            customer=self.customer,
            device_key="coldguard-test-get-2",
            display_name="Second Fridge",
            location="Storage",
            is_active=True
        )
        TemperatureReading.objects.create(
            device=device2,
            temperature=5.0,
            status="OK"
        )

        response = self.client.get(
            f'/api/temperature/?customer_id={self.customer.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2) 