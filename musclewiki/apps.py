from django.apps import AppConfig
from django.core.management import call_command


class MusclewikiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "musclewiki"

    def ready(self):
        try:
            call_command('loaddata', 'muscles.json')
        except:
            pass
