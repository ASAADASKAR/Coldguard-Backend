from rest_framework import serializers
from .models import Customer, Device


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    Validates and transforms customer data.
    """

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Email must be unique across all customers."""
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Customer with this email already exists."
            )
        return value


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for Device model.
    Validates and transforms device data.
    """

    class Meta:
        model = Device
        fields = [
            'id',
            'customer',
            'device_key',
            'name',
            'location',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_device_key(self, value):
        """Device key must be unique across all devices."""
        if Device.objects.filter(device_key=value).exists():
            raise serializers.ValidationError(
                "Device with this key already exists."
            )
        return value