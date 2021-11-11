from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

##Register New Users
@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):
        register = RegisterSerializer(data=request.data)
        register.create(request.data)
        return Response(status=status.HTTP_201_CREATED)
        