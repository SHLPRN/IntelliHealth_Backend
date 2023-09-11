import os
import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

json_file = open("../secrets.json")
SECRETS = json.load(json_file)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

SECRET_KEY = 'django-insecure-hcbfv)rj7!1vygq2j0=8ctcae_g!n93q1+)r@e*n2!23!6xo_l'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'IntelliHealth.middleware.AuthorizeMiddleware',
]


CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = ('*',)

CORS_ORIGIN_WHITELIST = (
    '*',
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

ROOT_URLCONF = 'IntelliHealth.urls'

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

WSGI_APPLICATION = 'IntelliHealth.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': SECRETS['HOST'],
        'PORT': SECRETS['PORT'],
        'NAME': SECRETS['DATABASE'],
        'USER': SECRETS['USER'],
        'PASSWORD': SECRETS['PASSWORD'],
    }
}


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

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMS
SMS_SECRET_ID = SECRETS['SMS_SECRET_ID']
SMS_SECRET_KEY = SECRETS['SMS_SECRET_KEY']
SMS_APPID = SECRETS['SMS_APPID']
SMS_SIGN_NAME = '个人开发网'
SMS_MODE = [
    SECRETS['SMS_MODE_1'],
]
