from book.models import Book, Borrowing
from utils.redis import redis_client
from django.utils import timezone
from datetime import timedelta
import json


class BookService:
    @staticmethod
    def list_available_books():
        return Book.objects.filter(is_available=True)

    @staticmethod
    def get_book_by_id(book_id):
        return Book.objects.get(id=book_id)

    @staticmethod
    def filter_books(publisher=None, category=None):
        queryset = Book.objects.all()
        if publisher:
            queryset = queryset.filter(publisher=publisher)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @staticmethod
    def borrow_book(book_id, user_id, days):
        try:
            book = Book.objects.select_for_update().get(id=book_id, is_available=True)
        except Book.DoesNotExist:
            return False, "Book not available or does not exist"

        borrow_date = timezone.now()
        return_date = borrow_date + timedelta(days=days)

        borrowing = Borrowing.objects.create(
            user_id=user_id,
            book=book,
            borrow_date=borrow_date,
            return_date=return_date
        )

        book.is_available = False
        book.save()

        # Notify backend about the change
        redis_client.publish('book_updates', json.dumps({
            'action': 'borrow',
            'book_id': book_id,
            'user_id': user_id,
            'borrow_date': borrow_date.isoformat(),
            'return_date': return_date.isoformat()
        }))

        return True, "Book borrowed successfully"
    
    
    @staticmethod
    def handle_book_update(data):
        if data['action'] == 'add':
            Book.objects.create(**data['book'])
        elif data['action'] == 'remove':
            Book.objects.filter(id=data['book_id']).delete()

    @staticmethod
    def start_listening_for_updates():
        pubsub = redis_client.pubsub()
        pubsub.subscribe('book_updates')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                BookService.handle_book_update(data)