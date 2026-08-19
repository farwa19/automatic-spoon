from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def delete_expired_accounts():
    # ✅ Import models only when the task runs
    from .models import Tests, AccountDeletionLog

    cutoff_date = timezone.now() - timedelta(days=27)
    expired_tests = Tests.objects.filter(
    created_at__lt=cutoff_date  # 'lt' means Less Than (older than)
)

    for test in expired_tests:
        AccountDeletionLog.objects.create(
            email=test.patient.email if test.patient else "Unknown",
            role="test_record",
            reason="27 days of inactivity"
        )
        test.delete()

    return f"Deleted {len(expired_tests)} expired test records"

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def run_command():
    print("🕒 Running delete_expired_accounts...")
    call_command('delete_expired_accounts')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_command, 'interval', days=1)
    scheduler.start()
    print("🔄 Started scheduler for delete_expired_accounts")
