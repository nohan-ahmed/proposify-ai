from django.db import models


class JobType(models.TextChoices):
    PROPOSAL = "proposal_generation", "Proposal Generation"
    RESUME = "resume", "Resume"
    COVER_LETTER = "cover_letter", "Cover Letter"
    OTHER = "other", "Other"


class JobStatus(models.TextChoices):
    QUEUED = "queued", "Queued"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELED = "canceled", "Canceled"


class ToneChoices(models.TextChoices):
    PROFESSIONAL = "professional", "Professional"
    FRIENDLY = "friendly", "Friendly"
    PERSUASIVE = "persuasive", "Persuasive"
    FORMAL = "formal", "Formal"
    CASUAL = "casual", "Casual"


class VisibilityChoices(models.TextChoices):
    PRIVATE = "private", "Private"
    SHARED = "shared", "Shared"
    PUBLIC = "public", "Public"