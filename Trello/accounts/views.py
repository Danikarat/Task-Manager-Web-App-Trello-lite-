from django.shortcuts import render
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer,ProfileSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Profile
# Create your views here.
# register view
class RegisterView(generics.CreateAPIView):
    serializer_class =  RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Custom login View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Logout View
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# profile view
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "email": user.email,
        })
    

# profile view
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class= ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    