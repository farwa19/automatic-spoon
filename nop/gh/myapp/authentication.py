from django.contrib.auth.backends import ModelBackend
from myapp.models import Name  # Import your custom user model
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Name.objects.get(username=username)
        except Name.DoesNotExist:
            return None

        if user.check_password(password):  # Manually verify the password
            return user
        return None
