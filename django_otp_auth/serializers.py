from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class OTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        # Skip all validation - just return the user
        # User is already authenticated in VerifyOTPView
        email = attrs.get('email')
        user, _ = User.objects.get_or_create(email=email)
        attrs['user'] = user
        return attrs
