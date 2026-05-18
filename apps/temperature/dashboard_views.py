"""
Dashboard API views for ColdGuard Frontend.
Provides read-only endpoints for current temperature, history, and alarms.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import TemperatureReading
from .constants import TemperatureStatus, TemperatureThreshold


class CurrentTemperatureView(APIView):
    """
    GET /api/dashboard/current/
    Returns the most recent temperature reading.

    Response:
    {
        "temperature": 4.2,
        "unit": "C",
        "status": "OK" | "ALARM_HIGH" | "ALARM_LOW",
        "timestamp": "2026-05-18T22:00:00Z",
        "device": "Fridge 1",
        "threshold_max": 8.0,
        "threshold_min": 1.0
    }
    """

    def get(self, request):
        reading = TemperatureReading.objects.select_related('device').first()

        if not reading:
            return Response({
                'temperature': None,
                'unit': 'C',
                'status': 'NO_DATA',
                'timestamp': None,
                'device': None,
                'threshold_max': TemperatureThreshold.MAX,
                'threshold_min': TemperatureThreshold.MIN,
            })

        return Response({
            'temperature': reading.temperature,
            'unit': 'C',
            'status': reading.status,
            'timestamp': reading.created_at.isoformat(),
            'device': reading.device.display_name,
            'threshold_max': TemperatureThreshold.MAX,
            'threshold_min': TemperatureThreshold.MIN,
        })


class TemperatureHistoryView(APIView):
    """
    GET /api/dashboard/history/?hours=24
    Returns temperature readings for the last N hours (default 24).

    Response: [
        {
            "temperature": 4.1,
            "timestamp": "2026-05-18T21:00:00Z",
            "status": "OK",
            "device": "Fridge 1"
        },
        ...
    ]
    """

    def get(self, request):
        hours = int(request.query_params.get('hours', 24))
        # Clamp to reasonable range
        hours = min(max(hours, 1), 168)  # 1h to 7 days

        since = timezone.now() - timedelta(hours=hours)
        readings = (
            TemperatureReading.objects
            .filter(created_at__gte=since)
            .select_related('device')
            .order_by('created_at')
        )

        data = [
            {
                'temperature': r.temperature,
                'timestamp': r.created_at.isoformat(),
                'status': r.status,
                'device': r.device.display_name,
            }
            for r in readings
        ]

        return Response(data)


class AlarmListView(APIView):
    """
    GET /api/dashboard/alarms/
    Returns all alarm readings (ALARM_HIGH or ALARM_LOW), grouped into
    alarm "events" — consecutive alarm readings are merged into one event.

    Response: [
        {
            "id": 1,
            "started_at": "2026-05-18T20:00:00Z",
            "resolved_at": "2026-05-18T20:15:00Z" | null,
            "max_temp": 9.1,
            "min_temp": 9.1,
            "status": "ALARM_HIGH",
            "message": "Temperature exceeded upper threshold (> 8.0°C)",
            "device": "Fridge 1"
        },
        ...
    ]
    """

    def get(self, request):
        # Get all readings ordered by time (newest first for display)
        all_readings = (
            TemperatureReading.objects
            .select_related('device')
            .order_by('created_at')
        )

        # Build alarm events by grouping consecutive alarm readings
        alarm_events = []
        current_event = None

        for reading in all_readings:
            is_alarm = reading.status in [
                TemperatureStatus.ALARM_HIGH,
                TemperatureStatus.ALARM_LOW,
            ]

            if is_alarm:
                if current_event is None:
                    # Start new alarm event
                    current_event = {
                        'started_at': reading.created_at,
                        'resolved_at': None,
                        'max_temp': reading.temperature,
                        'min_temp': reading.temperature,
                        'status': reading.status,
                        'device': reading.device.display_name,
                        'readings_count': 1,
                    }
                else:
                    # Extend current event
                    current_event['max_temp'] = max(
                        current_event['max_temp'], reading.temperature
                    )
                    current_event['min_temp'] = min(
                        current_event['min_temp'], reading.temperature
                    )
                    current_event['readings_count'] += 1
            else:
                if current_event is not None:
                    # Alarm resolved
                    current_event['resolved_at'] = reading.created_at
                    alarm_events.append(current_event)
                    current_event = None

        # If there's an ongoing alarm (never resolved)
        if current_event is not None:
            alarm_events.append(current_event)

        # Build response (newest first)
        alarm_events.reverse()
        data = []
        for i, event in enumerate(alarm_events, 1):
            if event['status'] == TemperatureStatus.ALARM_HIGH:
                message = (
                    f"Temperature exceeded upper threshold "
                    f"(> {TemperatureThreshold.MAX}°C)"
                )
            else:
                message = (
                    f"Temperature dropped below lower threshold "
                    f"(< {TemperatureThreshold.MIN}°C)"
                )

            data.append({
                'id': i,
                'started_at': event['started_at'].isoformat(),
                'resolved_at': (
                    event['resolved_at'].isoformat()
                    if event['resolved_at'] else None
                ),
                'max_temp': event['max_temp'],
                'min_temp': event['min_temp'],
                'status': event['status'],
                'message': message,
                'device': event['device'],
            })

        return Response(data)
