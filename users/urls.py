from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import PasswordResetConfirmView
from . import views


# Custom auth-related routes
auth_patterns = [
    path("registration/", views.CustomRegisterView.as_view(), name="custom_register"),
    path("verify-email/<uid>/<token>/", views.CustomVerifyEmailView.as_view(), name="custom_verify_email"),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('google/', views.GoogleLogin.as_view(), name='google_login')
]

# Router for UserSkill ViewSet
skill_router = DefaultRouter()
skill_router.register(r'user-skills', views.UserSkillViewSet, basename='user-skill')


# URL patterns
urlpatterns = [
    # include custom auth patterns
    path("", include(auth_patterns)),
    # include default dj-rest-auth patterns
    path("", include("dj_rest_auth.urls")),
    # include default dj-rest-auth registration patterns
    path("", include("dj_rest_auth.registration.urls")),
    # # include UserSkill routes
    path("", include(skill_router.urls)),
]
