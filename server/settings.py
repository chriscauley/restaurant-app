from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

import os
from django.core.management.utils import get_random_secret_key

def get_secret_key(BASE_DIR):
    key_path = os.path.join(BASE_DIR, 'server/.secret_key')
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            SECRET_KEY = f.read()
    else:
        SECRET_KEY = get_random_secret_key()
        with open(key_path, 'w') as f:
            f.write(SECRET_KEY)
            print('wrote secret key to', key_path)

    return SECRET_KEY

SECRET_KEY = get_secret_key(BASE_DIR)
DEBUG = True
ALLOWED_HOSTS = ['toptable.localhost']

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mailer',
    'django_registration',
    'social_django',
    'server.restaurant',
    'server.user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'server/templates')],
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

WSGI_APPLICATION = 'server.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Authentication
ACCOUNT_ACTIVATION_DAYS = 7
AUTH_USER_MODEL = 'user.User'
LOGIN_REDIRECT_URL='/'

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'server.user.social.get_avatar',
)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'client/dist')]
STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, '.media')
MEDIA_URL = '/media/'

# Other
EMAIL_BACKEND = "mailer.backend.DbBackend"

# machine specific settings
try:
    from .local_settings import *
except ImportError:
    pass

if os.environ.get('KILL_CSRF'):
    print("""
    KILL_CSRF is on.
    This is meant to be a temporary hack to make working in postman faster.
    Please enable asap.
    """)
    MIDDLEWARE = [s for s in MIDDLEWARE if s != 'django.middleware.csrf.CsrfViewMiddleware']