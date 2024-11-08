import os
import json
import boto3

from django.core.exceptions import ImproperlyConfigured
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
def get_secret():
    """
    Fetch secrets from AWS Secrets Manager.
    """
    secret_name = "my_secret_name"  # Gebe hier deinen Secret-Namen aus AWS Secrets Manager an
    region_name = "us-east-1"  # Region, in der dein Secret gespeichert ist

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise ImproperlyConfigured(f"Unable to fetch secrets: {e}")

    # Parse and return the secret JSON data
    secret = json.loads(get_secret_value_response["SecretString"])
    return secret

# Hole die Geheimdaten und speichere sie
try:
    secrets = get_secret()
except ImproperlyConfigured as e:
    print(e)
    secrets = {}

# Setze die Django-Settings
SECRET_KEY = secrets.get("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = secrets.get("DJANGO_DEBUG", "True").lower() == "true"


ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "https://orgagps.com",
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = ["https://orgagps.com"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'homepage',
    'accounts',
    'db',
    'locations',
    'custom_calendar',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orgagps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'orgagps.wsgi.application'

# Database configuration
# DATABASES = {
#     'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': BASE_DIR / 'db.sqlite3',
#      }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets.get('POSTGRES_DB', 'fallback_db'),
        'USER': secrets.get('POSTGRES_USER', 'fallback_user'),
        'PASSWORD': secrets.get('POSTGRES_PASSWORD', 'fallback_password'),
        'HOST': secrets.get('POSTGRES_HOST', 'localhost'),
        'PORT': secrets.get('POSTGRES_PORT', '5432'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email-Konfiguration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = secrets.get("MAIL_HOST", "smtp.fallback.com")
EMAIL_PORT = secrets.get("MAIL_PORT", 587)
EMAIL_USE_TLS = secrets.get("MAIL_USE_TLS", "true").lower() == "true"
EMAIL_HOST_USER = secrets.get("MAIL_USER", "fallback-user")
EMAIL_HOST_PASSWORD = secrets.get("MAIL_PASS", "fallback-pass")
DEFAULT_FROM_EMAIL = secrets.get("DEFAULT_FROM_EMAIL", "noreply@orgagps.com")
EMAIL_SUBJECT_PREFIX = secrets.get("EMAIL_SUBJECT_PREFIX", "[Orgagps] ")

# CORS und andere Django Settings wie in deiner Konfiguration
CORS_ALLOWED_ORIGINS = secrets.get("CORS_ALLOWED_ORIGINS", [
    "https://orgagps.com",
    "http://localhost:3000"
])

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'db.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
