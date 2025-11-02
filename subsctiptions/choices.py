from django.db import models

class SubscriptionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"

class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Credit Card"
    STRIPE = "stripe", "Stripe"
    OTHER = "other", "Other"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"