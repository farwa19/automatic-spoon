from django.contrib.auth.backends import ModelBackend
from .models import Name


class EmailBackend(ModelBackend):
    """Allow authentication with email instead of username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by email if email format is detected
            user = Name.objects.get(email=username)
        except Name.DoesNotExist:
            # Fall back to username
            try:
                user = Name.objects.get(username=username)
            except Name.DoesNotExist:
                return None

        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Name.objects.get(pk=user_id)
        except Name.DoesNotExist:
            return None
