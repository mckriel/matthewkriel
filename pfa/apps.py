from django.apps import AppConfig


class PfaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pfa'
    
    def ready(self):
        """Import signal handlers when the app is ready."""
        import pfa.models  # This imports the signal handlers
