from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegisterSerializer, UserSerializer, PasswordChangeSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        user = request.user

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Incorrect password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        update_session_auth_hash(request, user)  # Prevents logout on password change

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link sent."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, context={'request': request}, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class PublicUserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = user.profile
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)