from django.urls import path, include
from . import views

urlpatterns = [
    path('create-subscription-with-stripe/', views.CreateSubsctiptionWithStripeView.as_view(), name='create-subscription-with-stripe'),

]