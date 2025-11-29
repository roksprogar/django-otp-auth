import secrets
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from dj_rest_auth.views import LoginView

from .services import send_email
from .serializers import OTPLoginSerializer

User = get_user_model()

class RequestOTPView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'
    
    # Configurable attributes
    subject = None
    project_name = None
    
    def get_project_name(self):
        if self.project_name:
            return self.project_name
        return getattr(settings, 'OTP_AUTH_PROJECT_NAME', 'Lifetivation')

    def get_subject(self):
        if self.subject:
            return self.subject
        return f"Sign in to {self.get_project_name()}"

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate 6-character alphanumeric OTP
        alphabet = string.ascii_uppercase + string.digits
        otp = ''.join(secrets.choice(alphabet) for _ in range(6))
        

        # Store hashed OTP in cache with 5-minute expiry
        cache_key = f'otp_{email}'
        cache.set(cache_key, make_password(otp), timeout=300)

        # Render email content
        context = {
            'otp': otp,
            'project_name': self.get_project_name()
        }
        html_message = render_to_string('emails/otp_email.html', context)
        plain_message = render_to_string('emails/otp_email.txt', context)

        # Send OTP via email
        send_email(
            subject=self.get_subject(),
            message=plain_message,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        return Response({'message': 'OTP sent successfully'})

class VerifyOTPView(LoginView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_verify'
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response(
                {'error': 'Email and OTP are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify OTP
        cache_key = f'otp_{email}'
        stored_otp_hash = cache.get(cache_key)

        if not stored_otp_hash or not check_password(otp, stored_otp_hash):
            return Response(
                {'error': 'Invalid OTP'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Clear the OTP from cache
        cache.delete(cache_key)

        # We have overriden a serializer and used jwt in REST_AUTH settings.
        response = super().post(request)
        if 'refresh' in response.data:
            response.data.pop('refresh')
        return response
