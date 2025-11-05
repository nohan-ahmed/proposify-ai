from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

job_router = DefaultRouter()
job_router.register('jobs', views.JobViewSet, basename='job')

urlpatterns = [
    path('', include(job_router.urls)),
]