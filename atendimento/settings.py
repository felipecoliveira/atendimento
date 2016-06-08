# -*- coding: utf-8 -*-
"""
Django settings for atendimento project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from decouple import config
from dj_database_url import parse as db_url
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).ancestor(2)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aww-xq%lo(cuc17q!^0u@-&0&a7$=b$ua+54$l_50*z2v&tm=)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/?next='

# Application definition

ATENDIMENTO_APPS = [
    'servicos',
    'usuarios',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # extra apps
    'bootstrap3',
    'captcha',
    'crispy_forms',
    'djangobower',
    'django_extensions',
    'floppyforms',
    'sass_processor',
] + ATENDIMENTO_APPS

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'atendimento.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.messages.context_processors.messages',
                'atendimento.context_processors.usuario_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'atendimento.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url,
    )
}

# Email
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST = config('EMAIL_HOST', cast=str)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)
EMAIL_PORT = config('EMAIL_PORT', cast=int)


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# captcha config
CAPTCHA_IMAGE_SIZE = (130, 30)
CAPTCHA_FONT_SIZE = 30

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'pt-br'
LANGUAGES = (
    ('pt-br', u'Português'),
)

TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True
# DATE_FORMAT = 'N j, Y'
DATE_FORMAT = 'd/m/Y'
SHORT_DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%m-%d-%Y', '%Y-%m-%d')

LOCALE_PATHS = (
    'locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.child("collected_static")
STATICFILES_DIRS = (BASE_DIR.child("static"),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'sass_processor.finders.CssFinder',
)

MEDIA_ROOT = BASE_DIR.child("media")
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

BOWER_COMPONENTS_ROOT = BASE_DIR.child("bower")
BOWER_INSTALLED_APPS = (
    'bootstrap-sass#3.3.6',
    'components-font-awesome#4.5.0',
    'tinymce#4.3.3',
    'jquery-ui#1.11.4',
    'jquery-runner#2.3.3',
    'jQuery-Mask-Plugin#1.13.4',
    'jsdiff#2.2.1',
)

# Additional search paths for SASS files when using the @import statement
SASS_PROCESSOR_INCLUDE_DIRS = (BOWER_COMPONENTS_ROOT.child(
    'bower_components', 'bootstrap-sass', 'assets', 'stylesheets'),
)
