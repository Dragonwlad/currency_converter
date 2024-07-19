import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='django-insecure-secret_key')

DEBUG = os.getenv('DEBUG', default='True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Currency
NAME_MAX_LENGTH = 50

ISO_CODE_LENGTH = 3


# Data sources

FIAT_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

BEACON_API_KEY = 'Z0XwA6LYvN8RqGpUlM4Im4b68ZjP6h0K'
FIAT_BEACON_URL = f'https://api.currencybeacon.com/v1/latest?api_key={BEACON_API_KEY}&base=usd&symbols=ISO_LIST_VALUTE'



LOCAL_APPS = [
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'currency.apps.CurrencyConfig',
    'scheduler.apps.SchedulerConfig',

]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3-th party apps
    'rest_framework',
    'django_apscheduler',
    'drf_yasg',
    # local apps
    *LOCAL_APPS,
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

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ================================== DATABASE ==================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================================== REST_API ==================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# ================================== STATIC/MEDIA ==================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT_NAME = 'media'
MEDIA_ROOT = BASE_DIR / MEDIA_ROOT_NAME
MEDIA_URL = f'/{MEDIA_ROOT_NAME}/'

IMAGE_DIRECTORY = 'currency/images/'


# ================================== COMPONENTS/CONSTANTS ==========================

from config.components.apscheduler import *  # noqa
from config.components.logging import *  # noqa
from config.components.swagger import *  # noqa
from config.constans import *  # noqa
