from rest_framework import serializers
from .models import TemperatureReading
from .constants import TemperatureStatus, DS18B20

class TemperatureReadingSerializer(serializers.ModelSerializer):
    """
    Defines the expected JSON format from ESP32.
    Validates incoming data automatically.
    """

    class Meta:
        model = TemperatureReading
        fields = ['temperature', 'status', 'device_key']

    def validate_temperature(self, value):
        """Temperature must be within DS18B20 sensor range"""
        if value < DS18B20.MIN_RANGE or value > DS18B20.MAX_RANGE:
            raise serializers.ValidationError(
                f"Temperature out of sensor range "
                f"({DS18B20.MIN_RANGE} to {DS18B20.MAX_RANGE}°C)"
            )
        return value

    def validate_status(self, value):
        """Status must be one of the allowed values"""
        allowed = [TemperatureStatus.OK, TemperatureStatus.ALARM_HIGH, TemperatureStatus.ALARM_LOW]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {allowed}"
            )
        return value