from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    # allows browser to get list of plans and retrieve a single plan
    path('plans/', views.PlanListAPIView.as_view({'get': 'list'}), name='plan-list'),
    path('plans/<int:pk>/', views.PlanListAPIView.as_view({'get': 'retrieve'}), name='plan-detail'),
]