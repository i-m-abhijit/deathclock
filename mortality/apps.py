from django.apps import AppConfig


class MortalityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mortality'
    
    def ready(self):
        import mortality.signals
