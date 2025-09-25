from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh token to blacklist on logout")


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer  # for drf-spectacular introspection

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
