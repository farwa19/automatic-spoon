from django.apps import AppConfig
import os

class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"  # ⚠️ Ensure this matches your actual app folder name

    def ready(self):
        # 1. Import the updater we created
        from . import updater

        # 2. Prevent the scheduler from running twice (Django runs two processes in dev mode)
        if os.environ.get('RUN_MAIN'):
            updater.start()
