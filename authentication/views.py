from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
