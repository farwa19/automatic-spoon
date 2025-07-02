# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Name, AccountDeletionLog

@shared_task
def delete_expired_accounts():
    expired_patients = Name.objects.filter(role=Name.PATIENT)
    expired_patients = [p for p in expired_patients if p.is_expired()]
    
    for patient in expired_patients:
        AccountDeletionLog.objects.create(
            email=patient.email,
            role=patient.role,
            reason="27 days of inactivity"
        )
        patient.delete()
    
    return f"Deleted {len(expired_patients)} expired accounts"