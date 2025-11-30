SECRET_KEY = "test-secret-key"
ROOT_URLCONF = "tests.urls"


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.contenttypes",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django_otp_auth",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "otp_request": "1000/day",
        "otp_verify": "1000/day",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_AUTH = {
    "LOGIN_SERIALIZER": "django_otp_auth.serializers.OTPLoginSerializer",
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "jwt-auth",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
}
