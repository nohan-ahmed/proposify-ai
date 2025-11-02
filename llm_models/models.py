from django.db import models

# Create your models here.

class LLM(models.Model):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    provider_model = models.CharField(max_length=255)
    api_endpoint = models.CharField(max_length=255)
    tokens_per_request = models.IntegerField()
    max_tokens = models.IntegerField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name