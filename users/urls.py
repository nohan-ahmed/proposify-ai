from django.urls import path, include

from . import views


app_name = "users"

# Custom auth-related routes
auth_patterns = [
    path("registration/", views.CustomRegisterView.as_view(), name="custom_register"),
]


urlpatterns = [
    # include custom auth patterns
    path("", include((auth_patterns))),
    # include default dj-rest-auth patterns
    path("", include("dj_rest_auth.urls")),
    # include default dj-rest-auth registration patterns
    path("", include("dj_rest_auth.registration.urls")),
]
