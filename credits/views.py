from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from . import models
from . import serializers
from core.permissions import IsOwner
# Create your views here.

class PlanListAPIView(ModelViewSet):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]


class UserCreditListAPIView(ModelViewSet):
    queryset = models.UserCredit.objects.all()
    serializer_class = serializers.UserCreditSerializer
    permission_classes = [IsOwner]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        user = self.request.user
        return models.UserCredit.objects.filter(user=user)
