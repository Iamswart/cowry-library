from django.apps import AppConfig
import threading

class BookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book"
    
    def ready(self):
        from book.services import AdminBookService
        threading.Thread(target=AdminBookService.start_listening_for_updates, daemon=True).start()
