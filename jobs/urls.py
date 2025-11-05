from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('jobs/', views.JobViewSet.as_view({'get': 'list'}), name='job-list'),
    path('jobs/<int:pk>/', views.JobViewSet.as_view({'get': 'retrieve'}), name='job-detail'),
]