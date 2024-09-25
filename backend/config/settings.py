"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import sys
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(r19jmezop^@vvlo5ge7bk3sm+3i59785u&2u(2!$$*%iebf^v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TESTING = sys.argv[1:2] == ['test']
SAVE_DEFAULT_VALUES = False # must be true in production
# todo: add server host ip and next server ip
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-Party apps
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'storages',

    # Local apps
    'news',
    'realtors',
    'real_estate_offices',
    'advertisements',
    'users',
    'tools',
    'mainpages',
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



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], #[os.path.join(BASE_DIR , 'templates'), os.path.join(BASE_DIR), '../frontend/.next/server/app'],
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE':'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3'
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USERNAME"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv('DB_HOST'),
        'PORT':os.getenv('DB_PORT'),
    }
}

if TESTING:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('TEST_DB_NAME'),
        'USER': os.getenv('TEST_DB_USER'),
        'PASSWORD' : os.getenv('TEST_DB_PASSWORD'),
        'HOST': os.getenv('TEST_DB_HOST'),
        'PORT': os.getenv('TEST_DB_PORT'),
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 7*24*60*60
    },
    
    'auth': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 10*60
    },

    'ip' :{
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'TIMEOUT': 1*60*60,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# STATIC_URL = '_next/static/'
# STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, '../frontend/.next/static'),
    # os.path.join(BASE_DIR, '../frontend/public'),
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, '../frontend/.next')
# MEDIA_ROOT = os.path.join(BASE_DIR, '../frontend/public')
# MEDIA_URL = '/'


STORAGES = {
    'default':{
        'BACKEND': 'storages.backends.s3.S3Storage',
    },  

    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}


#  S3
AWS_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
S3_ENDPOINT_URL_WITH_BUCKET = f"{AWS_S3_ENDPOINT_URL.split('://')[0]}://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.split('://')[1]}"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]



# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    'access-control-allow-origin', 
    'content-type',
    'accept',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'authorization',
]

REST_FRAMEWORK ={
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],

    'DEFAULT_PERMISION_CLASSES': {
        'rest_framework.permisions.IsAuthenticated',
    },

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'common.utils.error_handlers.custom_error_handler',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30), 
}

if DEBUG:
    SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=7)

# django debug toolbar
INTERNAL_IPS = ['127.0.0.1']

if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        'debug_toolbar',
    ]

    MIDDLEWARE = [
        # 'middleware.debug_tool.DebugTool',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        *MIDDLEWARE,
    ]

# delay between two OTP code request for same number
NUMBER_DELAY = timedelta(minutes=1, seconds=30)


REALTOR_DEFAULT_SCORE = 4
ADVERTISEMENT_MEDIA_LIMIT = 6
SUGGESTED_SEARCH_LIMIT = 12