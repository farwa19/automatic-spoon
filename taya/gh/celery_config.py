# your_project/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gh')
app = Celery('gh')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'delete-expired-accounts-daily': {
        'task': 'myapp.tasks.delete_expired_accounts',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}
