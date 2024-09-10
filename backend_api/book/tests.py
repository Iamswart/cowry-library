from django.test import TestCase

# Create your tests here.
import unittest
from unittest.mock import patch, MagicMock
from book.services import AdminBookService
from book.models import Book

class TestAdminBookService(unittest.TestCase):

    @patch('book.services.Book.objects')
    @patch('book.services.redis_client')
    def test_add_book(self, mock_redis, mock_books):
        mock_book = Book(id=1, title='New Book', author='Author', publisher='Publisher', category='Category')
        mock_books.create.return_value = mock_book
        
        result = AdminBookService.add_book('New Book', 'Author', 'Publisher', 'Category')
        
        self.assertEqual(result, mock_book)
        mock_books.create.assert_called_once_with(
            title='New Book', 
            author='Author', 
            publisher='Publisher', 
            category='Category',
            is_available=True
        )
        mock_redis.publish.assert_called_once()

    @patch('book.services.Book.objects')
    @patch('book.services.redis_client')
    def test_remove_book(self, mock_redis, mock_books):
        mock_book = MagicMock()
        mock_books.get.return_value = mock_book
        
        result = AdminBookService.remove_book(1)
        
        self.assertTrue(result)
        mock_book.delete.assert_called_once()
        mock_redis.publish.assert_called_once()

    @patch('book.services.Book.objects')
    def test_list_unavailable_books(self, mock_books):
        mock_books.filter.return_value = [
            Book(id=1, title='Book 1', is_available=False),
            Book(id=2, title='Book 2', is_available=False)
        ]
        
        result = AdminBookService.list_unavailable_books()
        
        self.assertEqual(len(result), 2)
        mock_books.filter.assert_called_once_with(is_available=False)