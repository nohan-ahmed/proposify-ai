from django.urls import path, include
from . import views

urlpatterns = [
    path('create-subscription-with-stripe/', views.CreateSubsctiptionWithStripeView.as_view(), name='create-subscription-with-stripe'),
    path('stripe-webhook/', views.stripe_webhook_view, name='stripe-webhook'),
]