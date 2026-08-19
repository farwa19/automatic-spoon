from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import delete_expired_accounts

def run_job():
    print("🕒 Running delete_expired_accounts...")
    delete_expired_accounts()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_job, 'interval', seconds=30)
    scheduler.start()
    print("🔄 Started scheduler for delete_expired_accounts")
