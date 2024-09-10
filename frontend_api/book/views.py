from django.shortcuts import render
from rest_framework.views import APIView

from book.serializers import BookSerializer
from book.services import BookService
from rest_framework.response import Response

# Create your views here.
class BookListView(APIView):
    def get(self, request):
        books = BookService.list_available_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookDetailView(APIView):
    def get(self, request, book_id):
        book = BookService.get_book_by_id(book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class BookFilterView(APIView):
    def get(self, request):
        publisher = request.query_params.get('publisher')
        category = request.query_params.get('category')
        books = BookService.filter_books(publisher, category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookBorrowView(APIView):
    def post(self, request, book_id):
        user_id = request.data.get('user_id')
        days = int(request.data.get('days', 14))
        success, message = BookService.borrow_book(book_id, user_id, days)
        if success:
            return Response({"message": message})
        return Response({"message": message}, status=400)
