# ─── Temperature App Constants ───────────────────────
# Only used within the temperature app

from django.db import models


class TemperatureStatus:
    """Possible temperature reading statuses"""
    OK         = 'OK'
    ALARM_HIGH = 'ALARM_HIGH'   # Temperature > MAX
    ALARM_LOW  = 'ALARM_LOW'    # Temperature < MIN


class TemperatureThreshold:
    """
    Temperature limits for alarm triggering.
    Must match firmware TEMP_MAX and TEMP_MIN values.
    """
    MAX = 8.0   # Upper limit in Celsius
    MIN = 1.0   # Lower limit in Celsius


class TemperatureConfig:
    """Configuration for temperature monitoring"""
    MEASURE_INTERVAL = 60    # seconds between readings
    MAX_RETRIES      = 3     # HTTP retry attempts


class DS18B20:
    """
    DS18B20 sensor hardware specifications.
    Physical measurement range of the sensor.
    """
    MIN_RANGE = -55.0   # Minimum measurable temperature
    MAX_RANGE = 125.0   # Maximum measurable temperature


class TemperatureStatus:
    """Possible temperature reading statuses"""
    OK         = 'OK'
    ALARM_HIGH = 'ALARM_HIGH'   # Temperature > MAX
    ALARM_LOW  = 'ALARM_LOW'    # Temperature < MIN
    HEARTBEAT_FAILURE = 'HEARTBEAT_FAILURE'


class HeartbeatConfig:
    """
    Configuration for heartbeat monitoring.
    """
    TIMEOUT_MINUTES = 5    # Minutes before heartbeat alarm
    CHECK_INTERVAL  = 300  # Celery check interval in seconds

class LogLevel(models.TextChoices):
    """Log levels for device error logging."""
    INFO  = 'INFO',  'Info'
    WARN  = 'WARN',  'Warning'
    ERROR = 'ERROR', 'Error'


class DeviceErrorMessages:
    """
    Human-readable error messages for customers.
    Maps technical firmware errors to user-friendly messages.
    Used in dashboard and email notifications.
    """

    MESSAGES = {
        'Sensor not found — check wiring': {
            'de': 'Gerät nicht erreichbar — bitte Support kontaktieren',
            'en': 'Device unreachable — please contact support',
            'ar': 'جهاز الاستشعار غير متاح — يرجى التواصل مع الدعم',
        },
        'WiFi connection failed': {
            'de': 'Verbindungsproblem — WLAN prüfen',
            'en': 'Connection issue — check WiFi',
            'ar': 'مشكلة في الاتصال — تحقق من الواي فاي',
        },
        'Server unreachable after 3 retries': {
            'de': 'Gerät offline — Stromverbindung prüfen',
            'en': 'Device offline — check power connection',
            'ar': 'الجهاز غير متصل — تحقق من مصدر الطاقة',
        },
    }

    @classmethod
    def get(cls, technical_message: str, language: str = 'en') -> str:
        """
        Returns customer-friendly message for a technical error.
        Falls back to English if language not found.
        Falls back to technical message if not in dictionary.
        """
        messages = cls.MESSAGES.get(technical_message, {})
        return messages.get(language) or messages.get('en') or technical_message