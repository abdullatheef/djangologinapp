"""
Django settings for loginproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from mongoengine import *
connect('djangologinapp')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xohx7i9hyjzdr5=24x1rrfw!==y&!qtfkcey%e)0ts#*g@gb#-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine.django.mongo_auth',
    'djangologinapp',
    'sampleapp'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'loginproject.urls'

WSGI_APPLICATION = 'loginproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MONGO_BACKEND = True
AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,"djangologinapp/templates"),
    os.path.join(BASE_DIR,"sampleapp/templates"))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"djangologinapp/static"),
    os.path.join(BASE_DIR,"sampleapp/static"))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


APP_URL_DOMAIN = '/loginapp/'
LOGIN_URL = APP_URL_DOMAIN + 'login/'

try:
    from .private import *
except ImportError:
    pass

GOOGLE_SIGNIN = True
GOOGLE_CLIENT_ID = cl_id  # your client id
GOOGLE_CLIENT_SECRET = cl_secret # your client secret
GOOGLE_REDIRECT_URL = 'http://localhost:8000' + APP_URL_DOMAIN + 'login/'
GOOGLE_SCOPE = 'profile email'
GOOGLE_GRANT_TYPE = 'authorization_code'
GOOGLE_OAUTH2_URL = 'https://accounts.google.com/o/oauth2/auth?'





AFTER_LOGIN_URL = '/'
AFTER_LOGOUT_URL = '/'
SIGNIN_IMAGE_URL = 'http://i.huffpost.com/gen/1995938/thumbs/o-AHS-FREAK-SHOW-facebook.jpg'
SIGNUP_IMAGE_URL = 'http://i.huffpost.com/gen/1995938/thumbs/o-AHS-FREAK-SHOW-facebook.jpg'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}