from django.db import models
from users.models import User
from .choices import SubscriptionStatus, PaymentMethod, PaymentStatus
from credits.models import Plan
# Create your models here.

class Subsctiption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subsctiptions')
    plan = models.ForeignKey(to=Plan, on_delete=models.CASCADE, related_name='subsctiptions')
    status = models.CharField(max_length=100, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan} - {self.status}"
    

class Payment(models.Model):

    subscription = models.ForeignKey(Subsctiption, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for subscription #{self.subscription.id} by {self.user.username}"