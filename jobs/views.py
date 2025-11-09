from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import UserRateThrottle
from . import models
from . import serializers
from core.permissions import IsOwner
from . import prompts
from . import tasks

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class JobViewSet(ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [IsOwner]
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-queued_at")
    

class ProposalViewSet(ModelViewSet):
    queryset = models.Proposal.objects.all()
    serializer_class = serializers.ProposalSerializer
    permission_classes = [IsOwner]
    throttle_classes = [UserRateThrottle]
    
    def perform_create(self, serializer):
        #  Create Job
        job = models.Job.objects.create(
            user=self.request.user,
            llm=serializer.validated_data.get("llm"),
            job_type="proposal_generation",
            user_prompt=serializer.validated_data.get("prompt"),
            status="queued"
        )
        
        # Create empty Proposal linked to Job
        proposal = serializer.save(user=self.request.user, job=job)
        # Trigger async task to process the proposal
        tasks.process_proposal_async.delay(proposal.id)
        
        