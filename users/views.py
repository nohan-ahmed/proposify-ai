from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# Local imports
from . import models
from  . import serializers
from . import tasks
# Create your views here.


class CustomRegisterView(APIView):
    def post(self, request, format=None):
        serializer = serializers.CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Send verification email asynchronously
                tasks.send_verification_email.delay(user.id)
                # Return success response
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
