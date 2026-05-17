from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for Device model.
    """
    class Meta:
        model = Device
        fields = [
            'id',
            'customer',
            'device_key',
            'display_name',
            'location',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_device_key(self, value):
        """Device key must be unique."""
        if Device.objects.filter(device_key=value).exists():
            raise serializers.ValidationError(
                "Device with this key already exists."
            )
        return value