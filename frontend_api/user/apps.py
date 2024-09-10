from django.apps import AppConfig
import threading

class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
    
    def ready(self):
        from .services import UserService
        threading.Thread(target=UserService.start_listening_for_updates, daemon=True).start()
