from user.models import User
from utils.redis import redis_client
import json

class UserService:
    @staticmethod
    def enroll_user(email, firstname, lastname):
        user = User.objects.create(email=email, firstname=firstname, lastname=lastname)
        # Notify backend about the new user
        redis_client.publish('user_updates', json.dumps({
            'action': 'enroll',
            'user': {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
        }))
        return user

    @staticmethod
    def handle_user_update(data):
        if data['action'] == 'update':
            user = User.objects.get(id=data['user']['id'])
            for key, value in data['user'].items():
                setattr(user, key, value)
            user.save()

    @staticmethod
    def start_listening_for_updates():
        pubsub = redis_client.pubsub()
        pubsub.subscribe('user_updates')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                UserService.handle_user_update(data)