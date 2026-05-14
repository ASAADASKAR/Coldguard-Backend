from django.core.mail import send_mail
from django.conf import settings
from coldguard.constants import NotificationType
from .constants import TemperatureStatus


class NotificationService:
    """
    Handles all ColdGuard alarm notifications.
    Supports email now — WhatsApp and SMS in Phase 4.
    """

    @staticmethod
    def send_alarm(device_key, temperature, status, created_at,
                   notification_type=NotificationType.EMAIL):
        """
        Main entry point for sending alarm notifications.
        Routes to the correct notification channel.
        """
        if notification_type == NotificationType.EMAIL:
            NotificationService._send_email(
                device_key, temperature, status, created_at
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
    def _send_email(device_key, temperature, status, created_at):
        """
        Sends alarm email to the owner.
        Private method — only called by send_alarm().
        """

        # Determine alarm type
        if status == TemperatureStatus.ALARM_HIGH:
            alarm_type = 'TOO WARM'
            limit      = '> 8°C'
        else:
            alarm_type = 'TOO COLD'
            limit      = '< 1°C'

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

        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ALARM_EMAIL_RECIPIENT],
            fail_silently=False,
        )