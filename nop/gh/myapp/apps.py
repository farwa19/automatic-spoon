from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        # Only import tasks if absolutely required here
        from . import tasks  # assuming your scheduler is in myapp/tasks.py
        tasks.start()




