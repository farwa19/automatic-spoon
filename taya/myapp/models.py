from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


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
    created_at = models.DateTimeField(auto_now_add=True, blank=True)  # Allow blank for existing users
    last_activity = models.DateTimeField(auto_now=True, blank = True)  # Track last activity timestamp

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

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def is_expired(self):
        """Check if patient account is inactive for 27 days"""
        if self.role == self.PATIENT:
            expiration_date = self.created_at + timedelta(days=27)
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
class MedicalCondition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Tests(models.Model):

    patient = models.ForeignKey(
        Name,
        on_delete=models.CASCADE,
        related_name="tests"  # Meaningful related name
    )
    doctor = models.ForeignKey(
        'Doct',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor"  # Meaningful related name
    )
    past_history = models.ManyToManyField(MedicalCondition, blank=True)
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
    addquestion1 = models.CharField(max_length=1000, blank=True)
    addquestion2 = models.CharField(max_length=1000, blank=True)
    addquestion3 = models.CharField(max_length=1000, blank=True)
    addanswer1 = models.CharField(max_length=1000, blank=True)
    addanswer2 = models.CharField(max_length=1000, blank=True)
    addanswer3 = models.CharField(max_length=1000, blank=True)

    def save(self, *args, **kwargs):
        """Automatically set file size before saving."""
        if self.report_file:
            self.file_size = self.report_file.size  # Get file size in bytes
        super().save(*args, **kwargs)  # Store file size in bytes
# --- DOCTOR MODEL ---
class Doct(models.Model):
    # FIXED: Use settings.AUTH_USER_MODEL and REMOVED 'default=1' to prevent crash
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        null=True,
        blank=True
    )

    # FIXED: Standardized names
    full_name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, help_text="e.g., Cardiologist")
    profile_pic = models.ImageField(upload_to='doctor_pics/', default='default_doctor.png', blank=True)
    is_verified = models.BooleanField(default=False)
    patient_count = models.PositiveIntegerField(default=0)
    patients = models.ManyToManyField(
        Name,
        related_name='doctors',
        blank=True
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    hospital_name = models.CharField(max_length=200, default="City Hospital")
    languages = models.CharField(max_length=200, default="English, Urdu")

    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    patients_treated = models.CharField(max_length=20, default="1k+")
    success_rate = models.CharField(max_length=10, default="98%")
    rating = models.FloatField(default=4.5)
    review_count = models.PositiveIntegerField(default=0)
    consultation_fee = models.PositiveIntegerField(default=1000)
    @property
    def average_rating(self):
        """
        Returns the average rating for this product, or 0 if no reviews.
        """
        return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0



    def get_rating_counts(self):
        """
        Returns a dictionary with count for each rating (5,4,3,2,1)
        """
        from django.db.models import Count

        # Get counts for each rating
        rating_counts = self.reviews.values('rating').annotate(count=Count('id'))

        # Create a dictionary with all possible ratings initialized to 0
        result = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

        # Update with actual counts
        for item in rating_counts:
            result[item['rating']] = item['count']

        return result

    def get_rating_percentage(self, rating):
        """
        Returns percentage for a specific rating
        """
        total_reviews = self.reviews.count()
        if total_reviews == 0:
            return 0

        rating_counts = self.get_rating_counts()
        return (rating_counts[rating] / total_reviews) * 100

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialty}"

class DoctorEducation(models.Model):
    doctor = models.ForeignKey(Doct, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=10)

    class Meta: ordering = ['-start_year']
    def __str__(self): return self.degree

class DoctorExperience(models.Model):
    doctor = models.ForeignKey(Doct, on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=10)

    class Meta: ordering = ['-start_year']
    def __str__(self): return self.position

from django.db import models
from django.utils.translation import gettext_lazy as _

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='documents/')  # Upload PDF or DOCX files
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    doctor = models.ForeignKey(
        Doct,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
null=True
    )
    rating = models.PositiveSmallIntegerField()   # e.g. 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.doctor} ({self.rating})"

