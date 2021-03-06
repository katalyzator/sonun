"""
Django settings for mebel_app project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ql+!qx4adpv&-8xj3ib%=mpa&54m8-0m@u==-vln0q)e+5y1cm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']  # ['www.sonunmebel.com','185.243.247.47']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My apps
    'main',

    # Third part apps
    'captcha',
    'djcelery',
    'djcelery_email',
    'embed_video',

    # 'multilingual',
    # 'jsonify'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # HTML minify
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

]

HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ('^admin/')
KEEP_COMMENTS_ON_MINIFYING = True

ROOT_URLCONF = 'mebel_app.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

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
                'django.template.context_processors.i18n',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

WSGI_APPLICATION = 'mebel_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sonun',
        'USER': 'postgres',
        'PASSWORD': 'sonun_db_123@@!#!',
        'HOST': 'localhost',
        'PORT': '5432',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# LANGUAGE_CODE = 'en'
LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', _(u'RU')),
    ('en', _(u'EN'))
)

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Google Recaptcha

RECAPTCHA_PUBLIC_KEY = '6LfVHFQUAAAAANKOIsmxwnPBy0WKSwhcdA9m4CDO'
RECAPTCHA_PRIVATE_KEY = '6LfVHFQUAAAAAB3SI72aDhd8hcHd5cAbLhH-mwsT'
NOCAPTCHA = True

# Gmail SMTP server configs

APP_EMAIL = 'sonunmebel.kg@gmail.com'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CELERY_ACCEPT_CONTENT = ['json', 'pickle']

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = '587'

EMAIL_HOST_USER = os.environ.get('USER_EMAIL') or 'sonunmebel.kg'

EMAIL_HOST_PASSWORD = os.environ.get('PASS_EMAIL') or 'meder123'

EMAIL_USE_TLS = True  # TLS settings

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
