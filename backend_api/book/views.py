
from rest_framework.views import APIView
from rest_framework.response import Response
from book.services import AdminBookService
from .serializers import BookSerializer

class AdminAddBookView(APIView):
    def post(self, request):
        title = request.data.get('title')
        author = request.data.get('author')
        publisher = request.data.get('publisher')
        category = request.data.get('category')
        
        book = AdminBookService.add_book(title, author, publisher, category)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=201)

class AdminRemoveBookView(APIView):
    def delete(self, request, book_id):
        success = AdminBookService.remove_book(book_id)
        if success:
            return Response({"message": "Book removed successfully"}, status=204)
        return Response({"message": "Book not found"}, status=404)

class AdminUnavailableBooksView(APIView):
    def get(self, request):
        books = AdminBookService.list_unavailable_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)