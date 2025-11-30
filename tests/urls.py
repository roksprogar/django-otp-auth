from django.urls import path
from django_otp_auth.views import RequestOTPView, VerifyOTPView

urlpatterns = [
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]
