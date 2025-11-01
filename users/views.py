from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode

# rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
# allauth imports
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

# Local imports
from . import models
from  . import serializers
from . import tasks
from core.permissions import IsOwnerOrReadOnly

# Create your views here.


class CustomRegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'
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


class CustomVerifyEmailView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'
    def get(self, request, uid, token):
        try:
            # 1st decode the uid
            user_id = smart_str(urlsafe_base64_decode(uid))
            # 2nd get the user
            user = models.User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, models.User.DoesNotExist):
            # Invalid uid or user not found
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)


# Social Login Views here.
class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    


# UserSkill views here
class UserSkillViewSet(ModelViewSet):
    queryset = models.UserSkill.objects.all()
    serializer_class = serializers.UserSkillSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    # Override the get_queryset method to filter by user ID automatically
    def get_queryset(self):
        return models.UserSkill.objects.filter(user=self.request.user)
    
    # Override the perform_create method to set the user field automatically
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
# UserExperience views here.
class UserExperienceViewSet(ModelViewSet):
    queryset = models.UserExperience.objects.all()
    serializer_class = serializers.UserExperienceSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    # Override the get_queryset method to filter by user ID automatically
    def get_queryset(self):
        return models.UserExperience.objects.filter(user=self.request.user)
    
    # Override the perform_create method to set the user field automatically
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
# UserEducation views here.
class UserEducationViewSet(ModelViewSet):
    queryset = models.UserEducation.objects.all()
    serializer_class = serializers.UserEducationSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    # Override the get_queryset method to filter by user ID automatically
    def get_queryset(self):
        return models.UserEducation.objects.filter(user=self.request.user)
    
    # Override the perform_create method to set the user field automatically
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)