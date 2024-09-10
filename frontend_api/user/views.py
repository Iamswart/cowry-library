from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer
from user.services import UserService

# Create your views here.
class UserEnrollView(APIView):
    def post(self, request):
        email = request.data.get('email')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        user = UserService.enroll_user(email, firstname, lastname)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)