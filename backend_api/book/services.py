from book.models import Book, Borrowing
from utils.redis import redis_client
import json
from django.utils import timezone
from datetime import datetime

class AdminBookService:
    @staticmethod
    def add_book(title, author, publisher, category):
        book = Book.objects.create(
            title=title,
            author=author,
            publisher=publisher,
            category=category,
            is_available=True
        )
        # Notify frontend about the new book
        redis_client.publish('book_updates', json.dumps({
            'action': 'add',
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'publisher': book.publisher,
                'category': book.category,
                'is_available': book.is_available
            }
        }))
        return book

    @staticmethod
    def remove_book(book_id):
        book = Book.objects.get(id=book_id)
        book.delete()
        # Notify frontend about the removed book
        redis_client.publish('book_updates', json.dumps({
            'action': 'remove',
            'book_id': book_id
        }))
        return True

    @staticmethod
    def list_unavailable_books():
        return Book.objects.filter(is_available=False)
    
    @staticmethod
    def handle_book_update(data):
        if data['action'] == 'borrow':
            book = Book.objects.get(id=data['book_id'])
            Borrowing.objects.create(
                user_id=data['user_id'],
                book=book,
                borrow_date=datetime.fromisoformat(data['borrow_date']),
                return_date=datetime.fromisoformat(data['return_date'])
            )
            book.is_available = False
            book.save()

    @staticmethod
    def start_listening_for_updates():
        pubsub = redis_client.pubsub()
        pubsub.subscribe('book_updates')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                AdminBookService.handle_book_update(data)

