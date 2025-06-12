from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'walkease.user'

    def ready(self):
        import walkease.user.signals  # Registers signals for creating Profile objects.