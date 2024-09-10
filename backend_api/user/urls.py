from django.urls import path
from .views import AdminListUsersView, AdminListUsersWithBorrowedBooksView, AdminUserBorrowedBooksView, AdminUpdateUserView

urlpatterns = [
    path('admin/users/', AdminListUsersView.as_view(), name='admin-list-users'),
    path('admin/users/with-borrowed-books/', AdminListUsersWithBorrowedBooksView.as_view(), name='admin-users-with-borrowed-books'),
    path('admin/users/<int:user_id>/borrowed-books/', AdminUserBorrowedBooksView.as_view(), name='admin-user-borrowed-books'),
    path('admin/users/<int:user_id>/update/', AdminUpdateUserView.as_view(), name='admin-update-user'),
]