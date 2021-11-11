from django.shortcuts import render

from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny,))
class CheckServerView(APIView):
    """
    CheckServer
    """
    def get(self, request, format=None):
        """
        Get
        """
        return Response({"status": "ok", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, status=status.HTTP_200_OK)