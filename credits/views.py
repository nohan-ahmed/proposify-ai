from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from . import models
from . import serializers
# Create your views here.

class PlanListAPIView(ModelViewSet):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.PlanSerializer
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]