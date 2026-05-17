"""
ColdGuard Django Application

This module loads the Celery app when Django starts.
This ensures that Celery is always ready when Django is running,
enabling background tasks like the heartbeat checker.
"""

# Load Celery app when Django starts
# This is required so that shared_task decorator works correctly
from .celery import app as celery_app

__all__ = ('celery_app',)