from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


class TestAPIView(APIView):
    """Simple test endpoint to verify API is working"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "🚀 Stinet Digital API is working!",
            "status": "success",
            "version": "1.0.0",
            "endpoints": {
                "test": "/api/test/",
                "register": "/api/register/",
                "login": "/api/login/",
                "profile": "/api/profile/"
            }
        })


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                "success": True,
                "message": "🎉 Account created successfully!",
                "user": UserSerializer(user).data,
                "next_steps": "Please login with your credentials."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Registration failed",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login with JWT tokens"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "message": "✅ Login successful!",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "expires_in": "1 day"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Login failed",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get current user's profile (protected endpoint)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "success": True,
            "user": UserSerializer(user).data
        })