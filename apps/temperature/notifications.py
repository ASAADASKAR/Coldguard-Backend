from django.core.mail import send_mail
from django.conf import settings
from coldguard.constants import NotificationType, AlarmType
from .constants import TemperatureStatus, TemperatureThreshold, HeartbeatConfig


class NotificationService:
    """
    Handles all ColdGuard alarm notifications.
    Supports email now — WhatsApp and SMS in Phase 4.
    """

    @staticmethod
    def send_alarm(device_key, temperature, status, created_at,
                   recipient_email=None,
                   notification_type=NotificationType.EMAIL):
        """
        Main entry point for sending alarm notifications.
        Routes to the correct notification channel.

        Args:
            device_key (str): Unique device identifier.
            temperature (float): Current temperature in Celsius.
            status (str): ALARM_HIGH, ALARM_LOW or HEARTBEAT_FAILURE.
            created_at (datetime): Timestamp of the reading.
            recipient_email (str): Customer email address.
            notification_type (str): Channel to use (default: email).
        """
        if notification_type == NotificationType.EMAIL:
            NotificationService._send_email(
                device_key, temperature, status, created_at, recipient_email
            )

        elif notification_type == NotificationType.WHATSAPP:
            # TODO Phase 4: implement WhatsApp
            raise NotImplementedError(
                "WhatsApp notifications coming in Phase 4"
            )

        elif notification_type == NotificationType.SMS:
            # TODO Phase 4: implement SMS
            raise NotImplementedError(
                "SMS notifications coming in Phase 4"
            )

    @staticmethod
    def _send_email(device_key, temperature, status, created_at,
                    recipient_email=None):
        """
        Sends alarm email to the device owner.
        Private method — only called by send_alarm().

        Args:
            recipient_email (str): If None, uses ALARM_EMAIL_RECIPIENT from settings.
        """

        # Determine alarm type
        if status == TemperatureStatus.ALARM_HIGH:
            alarm_type = AlarmType.TOO_WARM
            limit      = f'> {TemperatureThreshold.MAX}°C'
        elif status == TemperatureStatus.ALARM_LOW:
            alarm_type = AlarmType.TOO_COLD
            limit      = f'< {TemperatureThreshold.MIN}°C'
        elif status == TemperatureStatus.HEARTBEAT_FAILURE:
            alarm_type = AlarmType.DEVICE_NOT_RESPONDING
            limit      = f'No signal for {HeartbeatConfig.TIMEOUT_MINUTES}+ minutes'

        # Build subject
        subject = f'[ColdGuard] ALARM — Temperature {alarm_type}!'

        # Build body
        message = f"""
ColdGuard Temperature Alarm
============================

ALARM TYPE : {alarm_type} ({limit})
DEVICE     : {device_key}
TEMPERATURE: {temperature}°C
STATUS     : {status}
TIME       : {created_at}

Please check your fridge immediately!

---
ColdGuard — Automatic Temperature Monitoring
This email was sent automatically. Do not reply.
        """

        # Use customer email if provided, otherwise fallback to settings
        recipient = recipient_email or settings.ALARM_EMAIL_RECIPIENT

        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )