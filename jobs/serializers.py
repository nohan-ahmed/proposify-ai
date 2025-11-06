from rest_framework import serializers
from . import models

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        fields = '__all__'
        read_only_fields = ['id', 'user', 'job', 'generated_text', 'tokens_prompt', 'tokens_completion', 'tokens_total', 'is_paid', 'created_at', 'updated_at']
        extra_kwargs = {
                'llm': {'required': True}
            }