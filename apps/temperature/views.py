from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TemperatureReading
from .serializers import TemperatureReadingSerializer
from .notifications import NotificationService
from .constants import TemperatureStatus
from apps.devices.models import Device


class TemperatureAPIView(APIView):
    """
    Receives temperature data from ESP32 devices.
    POST /api/temperature/
    """

    def post(self, request):

        # Get device key from header
        device_key = request.headers.get('X-Device-Key')

        # Validate device key
        if not device_key:
            return Response(
                {'error': 'Missing device key'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Find device in database
        try:
            device = Device.objects.get(
                device_key=device_key,
                is_active=True
            )
        except Device.DoesNotExist:
            return Response(
                {'error': 'Device not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get data from request
        data = request.data.copy()
        data['device'] = device.id

        # Validate with serializer
        serializer = TemperatureReadingSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save to database
        reading = serializer.save()

        # Send alarm if needed
        if reading.status in [
            TemperatureStatus.ALARM_HIGH,
            TemperatureStatus.ALARM_LOW
        ]:
            NotificationService.send_alarm(
                device_key=device_key,
                temperature=reading.temperature,
                status=reading.status,
                created_at=reading.created_at,
                recipient_email=device.customer.email
            )

        return Response(
            {
                'message': 'Temperature saved successfully',
                'id': reading.id,
                'device': device.name,
                'customer': device.customer.name,
                'temperature': reading.temperature,
                'status': reading.status,
                'created_at': reading.created_at,
            },
            status=status.HTTP_201_CREATED
        )