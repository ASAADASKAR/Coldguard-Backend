from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import TemperatureReading, DeviceLog
from .serializers import TemperatureReadingSerializer, DeviceLogSerializer
from .notifications import NotificationService
from .constants import TemperatureStatus
from apps.devices.models import Device


class TemperatureAPIView(APIView):
    """
    Receives temperature data from ESP32 devices.
    POST /api/temperature/ - ESP32 sends data
    GET  /api/temperature/ — Dashboard reads data
    """

    def get(self, request):
        """
        Returns temperature readings for a specific device or all devices of a customer.
        Used by the dashboard to display temperature history.

        Query params:
            device_key (optional): Returns readings for one specific device
            customer_id (optional): Returns readings for all devices of a customer

        One of the two parameters is required.

        Returns:
            200 — List of readings from last 24 hours, oldest first
            400 — Missing device_key or customer_id parameter
            404 — Device or customer not found or inactive

        Examples:
            GET /api/temperature/?device_key=coldguard-001
            GET /api/temperature/?customer_id=1
        """
        device_key = request.query_params.get('device_key')
        customer_id = request.query_params.get('customer_id')
        since = timezone.now() - timedelta(hours=24)

        if device_key:
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
            readings = TemperatureReading.objects.filter(
                device=device,
                created_at__gte=since
            ).order_by('created_at')

        elif customer_id:
            readings = TemperatureReading.objects.filter(
                device__customer_id=customer_id,
                device__is_active=True,
                created_at__gte=since
            ).order_by('created_at')

        else:
            return Response(
                {'error': 'device_key or customer_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TemperatureReadingSerializer(readings, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Receives temperature data from ESP32 device.
        Saves reading to database and sends alarm if needed.

        Headers:
            X-Device-Key (required): The unique device identifier

        Body:
            temperature (float): Temperature in Celsius
            status (str): OK | ALARM_HIGH | ALARM_LOW

        Returns:
            201 — Reading saved successfully
            400 — Invalid data
            401 — Missing device key
            404 — Device not found or inactive

        Example:
            POST /api/temperature/
            X-Device-Key: coldguard-001
            {"temperature": 4.5, "status": "OK"}
        """

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
            # Get pervious reading 
            previous = device.readings.order_by('-created_at').exclude(
                    id=reading.id
            ).first()

            # Only send if previous reading was OK or no previous reading
            was_ok = previous is None or previous.status == TemperatureStatus.OK

            if was_ok:
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
                'device': device.display_name,
                'customer': device.customer.name,
                'temperature': reading.temperature,
                'status': reading.status,
                'created_at': reading.created_at,
            },
            status=status.HTTP_201_CREATED
        )


class DeviceLogAPIView(APIView):
    """
    Manages device error logs.

    Endpoints:
        POST /api/logs/ — ESP32 sends error log
        GET  /api/logs/ — Dashboard reads error history

    Headers:
        X-Device-Key: device identifier
    """

    def post(self, request):
        """
        Receives error log from ESP32 device.

        Headers:
            X-Device-Key (required): device identifier

        Body:
            level (str): INFO | WARN | ERROR
            message (str): error description

        Returns:
            201 — Log saved
            401 — Missing device key
            404 — Device not found
        """
        device_key = request.headers.get('X-Device-Key')

        if not device_key:
            return Response(
                {'error': 'Missing device key'},
                status=status.HTTP_401_UNAUTHORIZED
            )

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

        data = request.data.copy()
        data['device'] = device.id

        serializer = DeviceLogSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {'message': 'Log saved successfully'},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        """
        Returns last 50 error logs for a device.

        Query params:
            device_key (required): device identifier

        Returns:
            200 — List of logs
            400 — Missing device_key
            404 — Device not found
        """
        device_key = request.query_params.get('device_key')
        lang = request.query_params.get('lang', 'en')

        if not device_key:
            return Response(
                {'error': 'device_key is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = Device.objects.get(
                device_key=device_key,
                is_active=True
            )
        except Device.DoesNotExist:
            return Response(
                {'error': 'Device not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        logs = DeviceLog.objects.filter(
            device=device
        )[:50]

        serializer = DeviceLogSerializer(
            logs,
            many=True,
            context={'lang': lang})
        return Response(serializer.data)