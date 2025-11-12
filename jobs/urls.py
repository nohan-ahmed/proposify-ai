from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'proposals', views.ProposalViewSet, basename='proposal')

urlpatterns = [
    path('jobs/', views.JobViewSet.as_view({'get': 'list'}), name='job-list'),
    path('jobs/<int:pk>/', views.JobViewSet.as_view({'get': 'retrieve'}), name='job-detail'),
    path('billing/', views.BillingLogViewSet.as_view({'get': 'list'}), name='billing-list'),
    path('billing/<int:pk>/', views.BillingLogViewSet.as_view({'get': 'retrieve'}), name='billing-detail'),
        
    path('', include(router.urls)),
]