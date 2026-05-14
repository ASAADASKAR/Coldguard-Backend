from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TemperatureReading
from .serializers import TemperatureReadingSerializer


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

        # Add device_key to request data
        data = request.data.copy()
        data['device_key'] = device_key

        # Validate with serializer
        serializer = TemperatureReadingSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save to database
        reading = serializer.save()

        return Response(
            {
                'message': 'Temperature saved successfully',
                'id': reading.id,
                'temperature': reading.temperature,
                'status': reading.status,
                'created_at': reading.created_at,
            },
            status=status.HTTP_201_CREATED
        )