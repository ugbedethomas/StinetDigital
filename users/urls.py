from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TestAPIView, RegisterView, LoginView, UserProfileView

urlpatterns = [
    # Public endpoints
    path('test/', TestAPIView.as_view(), name='test_api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # JWT token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Protected endpoints (require authentication)
    path('profile/', UserProfileView.as_view(), name='profile'),
]