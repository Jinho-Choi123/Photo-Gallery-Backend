from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

##Register New Users
@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):
        register = RegisterSerializer(data=request.data)
        register.is_valid(raise_exception=True)
        register.create(request.data)
        username = register.username

        return Response({"msg": "Account Created"}, status=status.HTTP_201_CREATED)

@permission_classes((AllowAny,))
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "username": str(username),
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)