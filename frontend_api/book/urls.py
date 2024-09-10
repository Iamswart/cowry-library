from django.urls import path
from book.views import BookListView, BookDetailView, BookFilterView, BookBorrowView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/filter/', BookFilterView.as_view(), name='book-filter'),
    path('books/<int:book_id>/borrow/', BookBorrowView.as_view(), name='book-borrow'),
]