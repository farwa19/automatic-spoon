from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Name, AccountDeletionLog

class Command(BaseCommand):
    help = 'Deletes patient accounts inactive for 27 days'
    
    def handle(self, *args, **options):
        expired_patients = Name.objects.filter(role=Name.PATIENT)
        expired_patients = [p for p in expired_patients if p.is_expired()]
        
        for patient in expired_patients:
            # Log before deletion
            AccountDeletionLog.objects.create(
                email=patient.email,
                role=patient.role,
                reason="27 days of inactivity"
            )
            patient.delete()
            self.stdout.write(f"Deleted inactive patient: {patient.email}")
        
        self.stdout.write(f"Deleted {len(expired_patients)} expired accounts")