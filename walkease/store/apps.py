from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"  # ✅ Ensure this matches the app name in `INSTALLED_APPS`
