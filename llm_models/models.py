from django.db import models
from . import choices
# Create your models here.

class LLM(models.Model):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, choices=choices.ProviderChoices.choices)
    provider_model = models.CharField(max_length=255)
    api_endpoint = models.CharField(max_length=255, blank=True, null=True)
    tokens_per_request = models.IntegerField()
    max_tokens = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name