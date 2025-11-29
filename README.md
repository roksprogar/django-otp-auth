# Django DRF OTP Auth

[![PyPI](https://img.shields.io/pypi/v/django-drf-otp-auth.svg)](https://pypi.org/project/django-drf-otp-auth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reusable Django app for email-based One-Time Password (OTP) authentication, designed for Django REST Framework (DRF) and integrated with `dj-rest-auth`.

## Why OTP?

Passwords are a pain. Users forget them, reuse them, and they are a prime target for attackers. Storing them securely is a liability.

**Django DRF OTP Auth** solves this by eliminating passwords entirely:

- 🧠 **No Memory Required**: Users don't need to remember complex passwords.
- 💾 **Zero Password Storage**: You don't have to worry about hashing, salting, or leaking passwords.
- 🔄 **Simplified Flows**: No more "Forgot Password" or "Reset Password" complexity.
- 🛡️ **Enhanced Security**: OTPs are short-lived and one-time use.

## Features

- 🔐 **Secure OTP Generation**: Cryptographically secure 6-character alphanumeric codes.
- ⚡ **Cache-Backed**: Fast and reliable storage for OTPs with automatic expiration (default 5 minutes).
- 📧 **Email Delivery**: Integrated email sending using Django's email backend.
- 🔌 **DRF Integration**: Ready-to-use API views for requesting and verifying OTPs.
- 🎫 **JWT Support**: Seamlessly integrates with `dj-rest-auth` to issue JWTs upon verification.
- ⚙️ **Configurable**: Customizable project name, email templates, and throttling.
- 🛡️ **Throttling**: Built-in support for `ScopedRateThrottle` to prevent abuse.

## Installation

```bash
pip install django-drf-otp-auth
```

Or using uv:

```bash
uv add django-drf-otp-auth
```

## Configuration

### 1. Add to `INSTALLED_APPS`

Add `django_otp_auth` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django_otp_auth',
    ...
]
```

### 2. Configure REST Framework & Auth

Ensure you have `dj-rest-auth` and `simplejwt` configured:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'otp_request': '5/hour',
        'otp_verify': '10/hour',
    }
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access-token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh-token',
}
```

### 3. Email Configuration

Configure your email backend in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'Your App <noreply@example.com>'
```

### 4. Optional Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `OTP_AUTH_PROJECT_NAME` | Project name used in emails | `'Lifetivation'` |

## Usage

### URL Configuration

Include the URLs in your project's `urls.py`:

```python
from django.urls import path, include
from django_otp_auth.views import RequestOTPView, VerifyOTPView

urlpatterns = [
    # ...
    path('auth/otp/request/', RequestOTPView.as_view(), name='otp_request'),
    path('auth/otp/verify/', VerifyOTPView.as_view(), name='otp_verify'),
    # ...
]
```

### API Endpoints

#### 1. Request OTP

**POST** `/auth/otp/request/`

Request a new OTP to be sent to the user's email.

**Payload:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully"
}
```

#### 2. Verify OTP

**POST** `/auth/otp/verify/`

Verify the received OTP. If successful, returns JWT access and refresh tokens (and sets them in cookies if configured).

**Payload:**
```json
{
  "email": "user@example.com",
  "otp": "ABC123"
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsIn...",
  "user": {
      "pk": 1,
      "email": "user@example.com",
      ...
  }
}
```

## Customization

### Email Templates

You can override the email templates by creating the following files in your project's `templates` directory:

- `templates/emails/otp_email.html`
- `templates/emails/otp_email.txt`

**Context available:**
- `otp`: The generated OTP code.
- `project_name`: The value of `OTP_AUTH_PROJECT_NAME`.

## Development

To run tests locally using `uv`:

```bash
uv run pytest
```
