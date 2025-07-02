from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Name(AbstractUser):  # Renamed to 'User' for better clarity
    PATIENT = 'patient'
    DOCTOR = 'doctor'

    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    ]

    MALE = 'male'
    FEMALE = 'female'

    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PATIENT)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, default="Anonymous")  # Provide default
    full_name = models.CharField(max_length=100, default="Unknown")  # Provide default
    age = models.IntegerField(default=18)  # Provide a reasonable default
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default=MALE)  # Provide default
    profession = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "full_name", "age", "sex", "profession", "address"]

    def __str__(self):
        return self.email
    def is_expired(self):
        """Check if patient account is inactive for 27 days"""
        if self.role == self.PATIENT:
            expiration_date = self.last_activity + timedelta(days=27)
            return timezone.now() > expiration_date
        return False  # Doctors don't expire
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = timezone.now()
        self.save()

class AccountDeletionLog(models.Model):
    """Track deleted accounts in admin"""
    email = models.EmailField()
    role = models.CharField(max_length=20)
    deletion_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, default="Inactivity")
    def __str__(self):
        return f"Deleted {self.role} account: {self.email}"

class Tests(models.Model):

    patient = models.ForeignKey(
        Name, 
        on_delete=models.CASCADE, 
        related_name="tests"  # Meaningful related name
    )
    past_history = models.CharField(max_length=50, blank=True,choices=[
        ('Diabetes Mellitus (DM)', 'Diabetes Mellitus (DM)'),
        ('Hypertension (HTN)', 'Hypertension (HTN)'),
        ('Heart problem', 'Heart problem')
    ])
    area_of_pain = models.CharField(max_length=50,blank=True, choices=[
        ('Neck', 'Neck'),
        ('Upper back', 'Upper back'),
        ('Lower back', 'Lower back')
    ])
    examination = models.CharField(max_length=50,blank=True)
    cause_of_pain = models.CharField(max_length=50,blank=True, choices=[
        ('Fever', 'Fever'),
        ('Injury', 'Injury'),
        ('Spontaneous', 'Spontaneous')
    ])
    pain_trouble = models.CharField(max_length=50, blank=True)
    aggravation = models.CharField(max_length=20,blank=True, choices=[
        ('Activity', 'Activity'),
        ('Rest', 'Rest')
    ])
    relief = models.CharField(max_length=20,blank=True, choices=[
        ('Activity', 'Activity'),
        ('Rest', 'Rest')
    ])
    numbness = models.CharField(max_length=50, blank=True,choices=[
        ('At rest', 'At rest'),
        ('At work', 'At work')
    ])
    neckPain = models.IntegerField(default=0, blank=True, null=True)
    armPain = models.IntegerField(default=0, blank=True, null=True)
    neckpain_inteference = models.CharField(max_length=50, blank=True)
    living_with_pain = models.CharField(max_length=50, blank=True)
    quality_of_life = models.CharField(max_length=50, blank=True)
    cutdownactivities = models.CharField(max_length=50, blank=True)
    neck_problems_work_leave = models.CharField(max_length=50, blank=True)
    arm = models.IntegerField(default=0, blank=True, null=True)
    walking_tolerance = models.PositiveIntegerField()
    support = models.BooleanField()
    
    GRIP_CHOICES = models.CharField(max_length=20,blank=True, choices=[
        ('Weak', 'Weak'),
        ('Good', 'Good')
    ])
    
    grip = models.CharField(max_length=10, choices=[
        ('Weak', 'Weak'),
        ('Good', 'Good')
    ], blank=True)  # Allow blank values
    
    audio = models.FileField(upload_to="test_audios/", null=True, blank=True)
    report_file = models.FileField(upload_to="mri_reports/", null=True, blank=True)  # Make it optional
    Bloodtest = models.FileField(upload_to="blood_reports/", null=True, blank=True)
    xray = models.FileField(upload_to="xray/", null=True, blank=True)
    ctscan = models.FileField(upload_to="ctscan/", null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
      # Allow blank values
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ilaj = models.CharField(max_length=1000,blank=True)

    def save(self, *args, **kwargs):
        """Automatically set file size before saving."""
        if self.report_file:
            self.file_size = self.report_file.size  # Get file size in bytes
        super().save(*args, **kwargs)  # Store file size in bytes

class Doct(models.Model):
    """Model representing doctors."""
    DENTIST = 'dentist'
    ORTHOPEDIC = 'orthopedic'

    SPECIALIZATION_CHOICES = [
        (DENTIST, 'Dentist'),
        (ORTHOPEDIC, 'Orthopedic'),
    ]

    specialization = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES,
        default=DENTIST,
    )
    patien = models.ForeignKey(
    Name, 
    on_delete=models.CASCADE, 
    related_name="patient", 
    null=True,  # Allow NULL values in the database
    blank=True  # Allow empty values in forms
)

    name = models.CharField(max_length=100)
   
    def __str__(self):
        return f"{self.name} ({self.get_specialization_display()})"
from django.db import models

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='documents/')  # Upload PDF or DOCX files
    uploaded_at = models.DateTimeField(auto_now_add=True)
