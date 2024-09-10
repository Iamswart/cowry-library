from django.db import models

from user.models import User
from utils.models import DatesMixin

# Create your models here.
class Book(DatesMixin):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    
    
class Borrowing(DatesMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()