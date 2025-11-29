import pytest
from django.urls import path
from django.core import mail
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django_otp_auth.views import RequestOTPView, VerifyOTPView

User = get_user_model()

User = get_user_model()

@pytest.mark.django_db
class TestOTPAuth:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.email = "test@example.com"
        self.password = "testpass123"
        # Create user
        self.user = User.objects.create_user(username="testuser", email=self.email, password=self.password)
        # Clear cache
        cache.clear()
        # Clear outbox
        mail.outbox = []

    def test_request_otp_success(self):
        """Test successful OTP request"""
        response = self.client.post('/request-otp/', {'email': self.email})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'message': 'OTP sent successfully'}
        
        # Verify email sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [self.email]
        assert "Sign in" in mail.outbox[0].subject
        
        # Verify OTP in cache
        cache_key = f'otp_{self.email}'
        assert cache.get(cache_key) is not None

    def test_request_otp_missing_email(self):
        """Test OTP request with missing email"""
        response = self.client.post('/request-otp/', {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_verify_otp_success(self):
        """Test successful OTP verification"""
        # First request OTP to populate cache (we can't easily mock the random OTP generation inside the view 
        # without patching, so let's just use the view logic or manually set cache if we knew the hash)
        
        # Let's manually set a known OTP in cache for testing
        from django.contrib.auth.hashers import make_password
        otp = "123456"
        cache.set(f'otp_{self.email}', make_password(otp), timeout=300)
        
        response = self.client.post('/verify-otp/', {'email': self.email, 'otp': otp})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'key' in response.data or 'access' in response.data # Depends on dj-rest-auth config
        
        # Verify OTP removed from cache
        assert cache.get(f'otp_{self.email}') is None

    def test_verify_otp_invalid(self):
        """Test OTP verification with invalid OTP"""
        from django.contrib.auth.hashers import make_password
        otp = "123456"
        cache.set(f'otp_{self.email}', make_password(otp), timeout=300)
        
        response = self.client.post('/verify-otp/', {'email': self.email, 'otp': '654321'})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid OTP'

    def test_verify_otp_expired_or_missing(self):
        """Test OTP verification when no OTP is in cache"""
        response = self.client.post('/verify-otp/', {'email': self.email, 'otp': '123456'})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid OTP'
