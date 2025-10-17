from django.apps import AppConfig


class AdoptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.adoptions'
    verbose_name = 'Adopciones'
    
    def ready(self):
        import apps.adoptions.signals