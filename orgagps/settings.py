import os
import json
import boto3
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

# AWS Secrets Manager verwenden, um Umgebungsvariablen sicher abzurufen
def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name=os.getenv("AW S_REGION"))
    try:
        response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise ImproperlyConfigured(f"Could not retrieve secret {secret_name}: {str(e)}")

    # Falls der Secret-Manager eine Secret-String zurückgibt
    if 'SecretString' in response:
        return json.loads(response['SecretString'])
    else:
        raise ImproperlyConfigured("Secret string not found in the AWS Secrets Manager response.")

# Secret aus AWS laden
secrets = get_secret("orgagps_app_secrets")

BASE_DIR = Path(__file__).resolve().parent.parent

# Abruf der geheimen Schlüssel aus AWS Secrets Manager
SECRET_KEY = secrets.get('DJANGO_SECRET_KEY')
DEBUG = secrets.get('DJANGO_DEBUG') == 'True'
ALLOWED_HOSTS = secrets.get('DJANGO_ALLOWED_HOSTS').split(',')

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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets.get('DB_NAME'),
        'USER': secrets.get('DB_USER'),
        'PASSWORD': secrets.get('DB_PASSWORD'),
        'HOST': secrets.get('DB_HOST'),
        'PORT': secrets.get('DB_PORT', '5432'),
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = secrets.get('MAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = secrets.get('MAIL')
EMAIL_HOST_PASSWORD = secrets.get('MAIL_PASS')
DEFAULT_FROM_EMAIL = 'noreply@orgagps.com'
EMAIL_SUBJECT_PREFIX = 'Password Recovery'

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
