from rest_framework import serializers
from .models import TemperatureReading


class TemperatureReadingSerializer(serializers.ModelSerializer):
    """
    Defines the expected JSON format from ESP32.
    Validates incoming data automatically.
    """

    class Meta:
        model = TemperatureReading
        fields = ['temperature', 'status', 'device_key']

    def validate_temperature(self, value):
        """Temperature must be between -55 and 125 (DS18B20 range)"""
        if value < -55 or value > 125:
            raise serializers.ValidationError(
                "Temperature out of sensor range (-55 to 125°C)"
            )
        return value

    def validate_status(self, value):
        """Status must be one of the allowed values"""
        allowed = ['OK', 'ALARM_HIGH', 'ALARM_LOW']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {allowed}"
            )
        return value