from rest_framework.views import APIView
from rest_framework.response import Response
from book.serializers import BorrowingSerializer
from user.services import AdminUserService
from .serializers import UserSerializer, UserWithBorrowedBooksSerializer

class AdminListUsersView(APIView):
    def get(self, request):
        users = AdminUserService.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class AdminListUsersWithBorrowedBooksView(APIView):
    def get(self, request):
        users = AdminUserService.list_users_with_borrowed_books()
        serializer = UserWithBorrowedBooksSerializer(users, many=True)
        return Response(serializer.data)

class AdminUserBorrowedBooksView(APIView):
    def get(self, request, user_id):
        borrowed_books = AdminUserService.get_user_borrowed_books(user_id)
        serializer = BorrowingSerializer(borrowed_books, many=True)
        return Response(serializer.data)
    
class AdminUpdateUserView(APIView):
    def put(self, request, user_id):
        data = request.data
        user = AdminUserService.update_user(user_id, **data)
        serializer = UserSerializer(user)
        return Response(serializer.data)