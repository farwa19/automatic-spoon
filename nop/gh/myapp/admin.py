from django.contrib import admin
from .models import Name, Doct, Tests, AccountDeletionLog
from django.utils import timezone
from datetime import timedelta

@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "date_joined", "is_expired", "is_staff")
    list_filter = ("role", "is_staff", "date_joined")
    search_fields = ("username", "email")
    readonly_fields = ("date_joined",)
    
    def is_expired(self, obj):
        """Custom admin column showing if patient account is expired"""
        return obj.role == Name.PATIENT and timezone.now() > (obj.date_joined + timedelta(days=27))
    is_expired.boolean = True
    is_expired.short_description = "Expired?"

@admin.register(Doct)
class DoctAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "patien")
    list_filter = ("specialization",)
    search_fields = ("name", "patien__name")
    raw_id_fields = ("patien",)  # Better for large user databases

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ("patient", "area_of_pain", "created_at", "walking_tolerance")
    list_filter = ("area_of_pain", "cause_of_pain", "created_at")
    search_fields = ("patient__name",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "uploaded_at")

@admin.register(AccountDeletionLog)
class DeletionLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'deletion_date', 'reason')
    readonly_fields = ('deletion_date',)
    list_filter = ('deletion_date', 'role')
    search_fields = ('email',)
    date_hierarchy = "deletion_date"