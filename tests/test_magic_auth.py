import pytest
from django.core import mail
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import check_password

User = get_user_model()

@pytest.mark.django_db
class TestMagicOTPAuth:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.OTP_AUTH_DISABLE_LOCAL_AUTH = True
        self.client = APIClient()
        self.email = "magic@example.com"
        # Clear cache
        cache.clear()
        # Clear outbox
        mail.outbox = []

    def test_magic_otp_request(self):
        """Test OTP request with Magic OTP enabled"""
        response = self.client.post('/request-otp/', {'email': self.email})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'message': 'OTP sent successfully'}
        
        # Verify email was NOT sent
        assert len(mail.outbox) == 0
        
        # Verify Magic OTP in cache
        cache_key = f'otp_{self.email}'
        stored_hash = cache.get(cache_key)
        assert stored_hash is not None
        assert check_password('000000', stored_hash)

    def test_magic_otp_verify(self):
        """Test verification with Magic OTP"""
        # First request to set the cache
        self.client.post('/request-otp/', {'email': self.email})
        
        # Verify with 000000
        response = self.client.post('/verify-otp/', {'email': self.email, 'otp': '000000'})
        
        assert response.status_code == status.HTTP_200_OK
        # Verify user was created/retrieved
        assert User.objects.filter(email=self.email).exists()

    def test_magic_otp_invalid_code(self):
        """Test that other codes fail even with Magic OTP enabled"""
        self.client.post('/request-otp/', {'email': self.email})
        
        response = self.client.post('/verify-otp/', {'email': self.email, 'otp': '123456'})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid OTP'
