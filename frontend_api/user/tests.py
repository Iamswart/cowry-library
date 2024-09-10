from django.test import TestCase

# Create your tests here.
import unittest
from unittest.mock import patch
from user.services import UserService
from user.models import User

class TestUserService(unittest.TestCase):

    @patch('user.services.User.objects')
    @patch('user.services.redis_client')
    def test_enroll_user(self, mock_redis, mock_users):
        mock_user = User(id=1, email='test@example.com', firstname='Test', lastname='User')
        mock_users.create.return_value = mock_user
        
        result = UserService.enroll_user('test@example.com', 'Test', 'User')
        
        self.assertEqual(result, mock_user)
        mock_users.create.assert_called_once_with(email='test@example.com', firstname='Test', lastname='User')
        mock_redis.publish.assert_called_once()