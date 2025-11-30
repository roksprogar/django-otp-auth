from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPAuthTests(TestCase):
    def test_sanity(self):
        """Basic sanity check to ensure test runner works."""
        self.assertEqual(1 + 1, 2)

    def test_app_installed(self):
        """Ensure the app is installed."""
        from django.apps import apps

        self.assertTrue(apps.is_installed("django_otp_auth"))
