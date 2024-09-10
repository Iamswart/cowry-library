from django.test import TestCase

# Create your tests here.
import unittest
from unittest.mock import patch
from user.services import AdminUserService
from user.models import User

class TestAdminUserService(unittest.TestCase):

    @patch('user.services.User.objects')
    def test_list_users(self, mock_users):
        mock_users.all.return_value = [
            User(id=1, email='user1@example.com'),
            User(id=2, email='user2@example.com')
        ]
        
        result = AdminUserService.list_users()
        
        self.assertEqual(len(result), 2)
        mock_users.all.assert_called_once()

    @patch('user.services.User.objects')
    def test_list_users_with_borrowed_books(self, mock_users):
        mock_users.filter.return_value.distinct.return_value = [
            User(id=1, email='user1@example.com'),
            User(id=2, email='user2@example.com')
        ]
        
        result = AdminUserService.list_users_with_borrowed_books()
        
        self.assertEqual(len(result), 2)
        mock_users.filter.assert_called_once_with(borrowing__isnull=False)