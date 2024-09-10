from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta

# Create your tests here.
import unittest
from unittest.mock import patch, MagicMock
from book.services import BookService
from book.models import Book, Borrowing

class TestBookService(unittest.TestCase):

    @patch('book.services.Book.objects')
    def test_list_available_books(self, mock_books):
        mock_books.filter.return_value = [
            Book(id=1, title='Book 1', is_available=True),
            Book(id=2, title='Book 2', is_available=True)
        ]
        
        result = BookService.list_available_books()
        
        self.assertEqual(len(result), 2)
        mock_books.filter.assert_called_once_with(is_available=True)

    @patch('book.services.Book.objects')
    def test_get_book_by_id(self, mock_books):
        mock_book = Book(id=1, title='Test Book')
        mock_books.get.return_value = mock_book
        
        result = BookService.get_book_by_id(1)
        
        self.assertEqual(result, mock_book)
        mock_books.get.assert_called_once_with(id=1)

    @patch('book.services.Book.objects')
    @patch('book.services.Borrowing.objects')
    @patch('book.services.redis_client')
    def test_borrow_book(self, mock_redis, mock_borrowings, mock_books):
        # Create a mock Book instance
        mock_book = MagicMock(spec=Book)
        mock_book.id = 1
        mock_book.is_available = True

        # Set up the mock for Book.objects.select_for_update().get()
        mock_books.select_for_update.return_value.get.return_value = mock_book

        # Set up the mock for Borrowing.objects.create()
        mock_borrowing = MagicMock(spec=Borrowing)
        mock_borrowings.create.return_value = mock_borrowing

        # Call the method under test
        success, message = BookService.borrow_book(1, 1, 7)

        # Assertions
        self.assertTrue(success)
        self.assertEqual(message, "Book borrowed successfully")
        self.assertFalse(mock_book.is_available)
        mock_book.save.assert_called_once()
        mock_borrowings.create.assert_called_once()
        mock_redis.publish.assert_called_once()

        # Check the arguments passed to Borrowing.objects.create()
        create_call_args = mock_borrowings.create.call_args[1]
        self.assertEqual(create_call_args['user_id'], 1)
        self.assertEqual(create_call_args['book'], mock_book)
        self.assertIsInstance(create_call_args['borrow_date'], datetime)
        self.assertIsInstance(create_call_args['return_date'], datetime)