from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import UserRateThrottle
from . import models
from . import serializers
from core.permissions import IsOwner

# Create your views here.

class JobViewSet(ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [IsOwner]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-queued_at")
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, attempts=1)