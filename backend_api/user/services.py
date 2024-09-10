from user.models import User
from book.models import Borrowing
from utils.redis import redis_client
import json

class AdminUserService:
    @staticmethod
    def list_users():
        return User.objects.all()

    @staticmethod
    def list_users_with_borrowed_books():
        return User.objects.filter(borrowing__isnull=False).distinct()

    @staticmethod
    def get_user_borrowed_books(user_id):
        return Borrowing.objects.filter(user_id=user_id).select_related('book')
    
    
    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.objects.get(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        redis_client.publish('user_updates', json.dumps({
            'action': 'update',
            'user': {
                'id': user.id,
                **kwargs
            }
        }))
        return user

    @staticmethod
    def handle_user_update(data):
        if data['action'] == 'enroll':
            User.objects.create(**data['user'])

    @staticmethod
    def start_listening_for_updates():
        pubsub = redis_client.pubsub()
        pubsub.subscribe('user_updates')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                AdminUserService.handle_user_update(data)