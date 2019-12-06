import os
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY: str = 'cru)q9q-!=#ip!)(i=rawgbjdfxiyrm+znk05iz=5p*w7r9(yh'

DEBUG: bool = bool(int(os.getenv('DEBUG', 1)))  # pylint: disable=invalid-envvar-default

ALLOWED_HOSTS: List[str] = ['*']  # On develop only

INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'pitter',
    'api_client',
]

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pitter.middleware.ErrorHandlerMiddleware',
    'pitter.middleware.AuthorizationMiddleware',
]

ROOT_URLCONF: str = 'pitter.urls'

TEMPLATES: List[Dict[str, Union[Dict[str, List[str]], List, bool, str]]] = [
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

DATABASES: Dict[str, Dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE', 'postgres'),
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('PGPASSWORD', 'postgres'),
        'HOST': os.getenv('PGHOST', 'localhost'),
        'PORT': os.getenv('PGPORT', '5432'),
    }
}

WSGI_APPLICATION: str = 'pitter.wsgi.application'
USE_X_FORWARDED_HOST: bool = True
SECURE_PROXY_SSL_HEADER: Tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE: str = 'en-us'

TIME_ZONE: str = 'Europe/Moscow'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

STATICFILES_DIRS: List[str] = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL: str = '/static/'

STATIC_ROOT: str = '/static'

# DRF

REST_FRAMEWORK: Dict[str, Union[List[str], str]] = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'EXCEPTION_HANDLER': 'pitter.middleware.custom_exception_handler',
}

# Swagger

SWAGGER_SETTINGS: Dict[str, Union[Dict[str, Dict[str, str]], bool]] = {
    'DEEP_LINKING': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
        'X-Device-Info': {'type': 'apiKey', 'name': 'X-Device-Info', 'in': 'header'},
    },
}

ASYNCHRONOUS_SERVICE_URL: str = 'http://pitter_async:8118/api/pitter/v1/recognize'

JSON_WEB_TOKEN_LIFETIME: timedelta = timedelta(hours=1)

JSON_WEB_TOKEN_PRIVATE_KEY: bytes = open('token_keys/id_rsa', 'rb').read()

JSON_WEB_TOKEN_PUBLIC_KEY: bytes = open('token_keys/id_rsa.pub', 'rb').read()
