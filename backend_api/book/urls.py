from django.urls import path
from .views import AdminAddBookView, AdminRemoveBookView, AdminUnavailableBooksView

urlpatterns = [
    path('admin/books/add/', AdminAddBookView.as_view(), name='admin-add-book'),
    path('admin/books/<int:book_id>/remove/', AdminRemoveBookView.as_view(), name='admin-remove-book'),
    path('admin/books/unavailable/', AdminUnavailableBooksView.as_view(), name='admin-unavailable-books'),
]