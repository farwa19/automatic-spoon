from celery import shared_task
from django.utils import timezone

@shared_task
def delete_expired_accounts():
    # ✅ Import models only when the task runs
    from .models import Name, AccountDeletionLog
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

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def run_command():
    print("🕒 Running delete_expired_accounts...")
    call_command('delete_expired_accounts')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_command, 'interval', days=1)  # or days=1
    scheduler.start()
    print("🔄 Started scheduler for delete_expired_accounts")