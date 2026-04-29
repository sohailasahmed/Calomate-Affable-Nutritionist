"""Django settings for core project."""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------
# SECRET KEY
# ---------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")

API_KEY = os.getenv("API_KEY")

# ---------------------------------------------------
# DEBUG
# ---------------------------------------------------
DEBUG = os.getenv("DEBUG", "False") == "True"

# ---------------------------------------------------
# ALLOWED HOSTS
# ---------------------------------------------------
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

# ---------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------
INSTALLED_APPS = [
    'users',
    'diet',
    'analytics',
    'chatbot',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ---------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # whitenoise for static files deployment
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------
# ROOT
# ---------------------------------------------------
ROOT_URLCONF = 'core.urls'

# ---------------------------------------------------
# TEMPLATES
# ---------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ---------------------------------------------------
# WSGI
# ---------------------------------------------------
WSGI_APPLICATION = 'core.wsgi.application'

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------
if os.getenv("DATABASE_URL"):
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.parse(
            os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------
# PASSWORDS
# ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# ---------------------------------------------------
# LANGUAGE / TIME
# ---------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True

# ---------------------------------------------------
# STATIC
# ---------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------
# MEDIA
# ---------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
LOGIN_URL = '/register/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/'

# ---------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SECURE_REFERRER_POLICY = "same-origin"

# ---------------------------------------------------
# DEFAULT PK
# ---------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'