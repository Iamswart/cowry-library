from rest_framework import serializers

from book.serializers import BorrowingSerializer
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname']
        
        
class UserWithBorrowedBooksSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowingSerializer(many=True, source='borrowing_set')

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'borrowed_books']