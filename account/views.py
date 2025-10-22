from decouple import config
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .models import User


# Create your views here.

class UserRegisterView(APIView):
    """
    This api view is used to register a new user,

    Parameters:

        -phone number (should be 11 digits, string)
        -email
        -full name
        -password
    """

    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            data = ser_data.validated_data
            User.objects.create_user(phone_number=data['phone_number'], full_name=data['full_name'],
                                     email=data['email'], password=data['password'])
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    This api view is used to login a user,

    Parameters:

        -phone number (should be 11 digits, string)
        -password

    """

    serializer_class = UserLoginSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            data = ser_data.validated_data
            user = authenticate(request, phone_number=data['phone_number'], password=data['password'])
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            return Response({'message': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    This api view is used to logout a user,
    """

    def post(self, request):
        logout(request)
