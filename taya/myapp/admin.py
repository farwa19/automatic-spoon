from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone
from datetime import timedelta
from .models import (
    Name,
    Doct,
    DoctorEducation,
    DoctorExperience,
    Review,
    Tests,
    MedicalCondition,
    AccountDeletionLog,
    UploadedDocument
)

# --- 1. Global Admin Panel Settings ---
admin.site.site_header = "Care Connect Admin"
admin.site.site_title = "Care Connect Admin Portal"
admin.site.index_title = "Welcome to Hospital Management"


# --- 2. Inlines (Education & Experience for Doctors) ---
class EducationInline(admin.TabularInline):
    model = DoctorEducation
    extra = 1

class ExperienceInline(admin.TabularInline):
    model = DoctorExperience
    extra = 1


# --- 3. User/Patient Admin Customization ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Name
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Name
        fields = ("email", "username")


@admin.register(Name)
class NameAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Name
    list_display = ("username", "email", "role", "date_joined", "is_staff")
    list_filter = ("role", "is_staff", "date_joined")
    search_fields = ("username", "email")
    ordering = ("email",)
    readonly_fields = ("date_joined",)

    def is_expired(self, obj):
        """Custom admin column showing if patient account is expired"""
        if obj.role == Name.PATIENT:
            return timezone.now() > (obj.date_joined + timedelta(days=27))
        return False

    is_expired.boolean = True
    is_expired.short_description = "Expired?"

    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )


# --- 4. Doctor Admin Customization ---
@admin.register(Doct)
class DoctAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'specialty',
        'hospital_name',
        'rating',
        'consultation_fee',
        'is_verified'
    )

    list_filter = ('specialty', 'is_verified', 'hospital_name', 'languages')
    search_fields = ('full_name', 'specialty', 'email')
    list_editable = ('is_verified', 'consultation_fee')
    list_per_page = 20

    # Attach the inlines here
    inlines = [EducationInline, ExperienceInline]

    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'full_name', 'profile_pic', 'email', 'phone', 'bio')
        }),
        ('Professional Details', {
            'fields': ('specialty', 'hospital_name', 'languages', 'consultation_fee')
        }),
        ('Stats (Read Only)', {
            'fields': ('rating', 'review_count', 'patients_treated', 'success_rate'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_verified', 'patient_count')
        }),
    )


# --- 5. Review Admin Customization ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'rating', 'created_at_formatted')
    list_filter = ('rating', 'created_at')
    search_fields = ('doctor__full_name', 'user__username', 'comment')
    readonly_fields = ('created_at',)

    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")
    created_at_formatted.short_description = 'Date'


# --- 6. Tests Admin Customization ---
@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ("patient", "area_of_pain", "created_at", "walking_tolerance")
    list_filter = ("area_of_pain", "cause_of_pain", "created_at")
    search_fields = ("patient__name",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "uploaded_at")


# --- 7. Simple Registrations ---
admin.site.register(MedicalCondition)
admin.site.register(AccountDeletionLog)
admin.site.register(UploadedDocument)
