"""
Django settings for jongole project.
Updated for Microservice Authentication with Brainless.
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This is Jongole's internal key (for sessions/CSRF)
SECRET_KEY = 'django-insecure-bh$qqul13*%1)bd)^#%o&6=_v=u7rp#ii0r92%^-hvc!w02ba_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 🟢 UPDATE: Allow local connections
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Internal Apps
    'core',

    # Third Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jongole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jongole.wsgi.application'


# Database
# Note: Jongole uses its own database to store Profiles.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- MICROSERVICE CONFIGURATION ---

# 🔑 This MUST match Brainless's SECRET_KEY
BRAINLESS_SECRET_KEY = 'django-insecure-vy4cfge=$amqyk2&hl_j#(n@0563cb%70-4b^^^q8w=*jw2x0_'
BRAINLESS_BASE_URL = "http://localhost:8000"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 🟢 IMPORTANT: Using JWTTokenUserAuthentication for Stateless Auth.
        # This allows Jongole to trust the token without a local User table lookup.
        "rest_framework_simplejwt.authentication.JWTTokenUserAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),

    # 🔑 UUID-based identity synced with Brainless
    "USER_ID_FIELD": "user_uuid",
    "USER_ID_CLAIM": "user_uuid",

    # Use Brainless's key to verify incoming tokens
    "SIGNING_KEY": BRAINLESS_SECRET_KEY, 
    "ALGORITHM": "HS256",
}