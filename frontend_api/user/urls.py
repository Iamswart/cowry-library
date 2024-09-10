from django.urls import path
from .views import UserEnrollView

urlpatterns = [
    path('users/enroll/', UserEnrollView.as_view(), name='user-enroll'),
]