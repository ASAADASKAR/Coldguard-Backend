"""
ColdGuard Celery Configuration

Celery is used for running background tasks automatically.
Currently used for:
- Heartbeat checker: runs every 5 minutes to detect
  devices that have stopped sending data (power outage, WiFi failure)
"""

import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coldguard.settings')

# Create Celery app instance
app = Celery('coldguard')

# Load Celery configuration from Django settings
# All Celery settings in settings.py must start with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all Django apps
# Looks for tasks.py in every installed app
app.autodiscover_tasks()