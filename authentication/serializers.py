from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # User is inactive until email is verified
        )

        # Generate token & send verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify: {verification_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return user
