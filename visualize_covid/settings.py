"""
Django settings for covid19live project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['visualizecovid.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'dashboard',
    'crispy_forms',
    'django_celery_beat',
    'django.contrib.humanize'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'visualize_covid.urls'

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

WSGI_APPLICATION = 'visualize_covid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

django_heroku.settings(locals())

if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)
   MIDDLEWARE += (
       'debug_toolbar.middleware.DebugToolbarMiddleware',
   )

   INSTALLED_APPS += (
       'debug_toolbar',
   )

   DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]

   DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
   }

# celery
CELERY_BROKER_URL = 'redis://localhost:6379'  
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'   
FORKED_BY_MULTIPROCESSING = 1

# celery_beat
CELERY_BEAT_SCHEDULE = {
    'asdf-every-10-seconds': {
        'task': 'tasks.asdf',
        'schedule': 10.0,
    },
    'update_db-every-hour': {
        'task': 'tasks.update_db',
        'schedule': 3600.0,
    }
}
