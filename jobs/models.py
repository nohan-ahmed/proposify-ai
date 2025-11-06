from django.db import models
from django.utils import timezone
from users.models import User
from llm_models.models import LLM
from .choices import (
    ToneChoices,
    JobType,
    JobStatus,
    VisibilityChoices
    
)



class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    llm = models.ForeignKey(LLM, on_delete=models.SET_NULL, null=True)
    job_type = models.CharField(max_length=40, choices=JobType.choices)

    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.QUEUED)

    user_prompt = models.JSONField()  # e.g. { job_prompt, tone, language }
    result_meta = models.JSONField(null=True, blank=True)

    attempts = models.PositiveIntegerField(default=0)
    error = models.TextField(null=True, blank=True)

    queued_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "jobs"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Job ID: {self.id} - ({self.job_type}) - Status: {self.status}"


class Proposal(models.Model):
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, related_name="proposal")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    llm = models.ForeignKey(LLM, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=255, null=True, blank=True)
    prompt = models.TextField()
    language = models.CharField(max_length=10, default="en")

    tone = models.CharField(max_length=20, choices=ToneChoices.choices)

    generated_text = models.TextField()

    visibility = models.CharField(max_length=10, choices=VisibilityChoices.choices, default=VisibilityChoices.PRIVATE)

    tokens_prompt = models.PositiveIntegerField(default=0)
    tokens_completion = models.PositiveIntegerField(default=0)
    tokens_total = models.PositiveIntegerField(default=0)

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "proposals"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["visibility"]),
        ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return f"Proposal for {self.user.email}"


class BillingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    llm = models.ForeignKey(LLM, on_delete=models.SET_NULL, null=True)

    tokens_prompt = models.PositiveIntegerField()
    tokens_completion = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=12, decimal_places=4)
    currency = models.CharField(max_length=10, default="USD")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "billing_logs"
        indexes = [
            models.Index(fields=["user"]),
        ]
