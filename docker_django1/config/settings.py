import os
from pathlib import Path
from dataclasses import dataclass

from typing import List

from celery import Celery

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = None

DEBUG = True

ALLOWED_HOSTS = ["*"]

"""
===============================================================================
Administration site Header, subheader, HTML title
===============================================================================
"""
# Заменить на свое название

ADMIN_SITE_HEADER = 'Header тестового приложения'
ADMIN_INDEX_TITLE = 'Index Title тестового приложения'
ADMIN_SITE_TITLE = 'Site Title тестового приложения'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'simple_history',
    'docker_django1.apps.core',
    'docker_django1.apps.user',
    'debug_toolbar',  # django debug
    'django_celery_beat',  # celery beat
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # keep it first
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # django_debug
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # keep it last
]

INTERNAL_IPS = [
    '0.0.0.0',
]


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

ROOT_URLCONF = 'docker_django1.apps.core.web.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.normpath(os.path.join(os.path.dirname(BASE_DIR), 'static'))
STATICFILES_DIRS: List[str] = []
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates'],
        'DIRS': STATICFILES_DIRS,
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
# diable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '@memcached_dd:11211',
#     }
# }

WSGI_APPLICATION = 'docker_django1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': os.getenv('DB_NAME'),
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'ENGINE': 'django.db.backends.postgresql',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': int(os.getenv('POSTGRES_CONN_MAX_AGE', 0)),
    },
}

# Logging
LOGGING_DIVIDER = '|'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': f'[%(asctime)s] {LOGGING_DIVIDER} %(processName)-15s {LOGGING_DIVIDER}'
            f' %(levelname)-8s {LOGGING_DIVIDER} %(lineno)-5d {LOGGING_DIVIDER}'
            f' %(name)s {LOGGING_DIVIDER} %(module)s {LOGGING_DIVIDER}'
            f' %(funcName)s {LOGGING_DIVIDER} %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'short': {
            'class': 'logging.Formatter',
            'format': '[%(asctime)s] - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        # FOR DB
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'INFO' if not DEBUG else 'DEBUG',
        # },
        '': {
            'handlers': ['console'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# custom user model
AUTH_USER_MODEL = 'user.User'


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

# DRF (Django Rest Framework)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'docker_django1.apps.core.pagination.paginators.FasterPageNumberPagination',
    'DATETIME_FORMAT': '%s',  # using unix timestamp for datetime fields serialization
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'worldskills_express.apps.base.auth.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'EXCEPTION_HANDLER': 'docker_django1.apps.core.views.exceptions.custom_exception.custom_exception_handler',
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': int(os.getenv('DJANGO_PAGE_SIZE', 100)),
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)

"""
===============================================================================
Redis specific settings
===============================================================================
"""
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

REDIS_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
"""
celery -A docker_django1.config.settings worker
"""

"""
===============================================================================
RabbitMQ specific settings
===============================================================================
"""
RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')

"""
===============================================================================
Celery specific settings
New celery configuration params

https://docs.celeryproject.org/en/stable/userguide/configuration.html#new-lowercase-settings

===============================================================================
"""
RABBITMQ_BROKER_URL = (
    f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'
)

CELERY_APP = Celery(
    'dd', broker=RABBITMQ_BROKER_URL, backend='rpc://', result_persistent=False
)
CELERY_APP.config_from_object('django.conf:settings', namespace='CELERY')
CELERY_APP.autodiscover_tasks(lambda: INSTALLED_APPS)

CELERY_APP.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=TIME_ZONE,
    enable_utc=True,  # task_ignore_result=False,
    # to debug task
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
)


CELERY_LOGGERS = {
    'celery': {
        'handlers': [
            'console',
        ],
        'propagate': False,
    },
}
# noinspection PyTypeChecker
LOGGING['loggers'].update(CELERY_LOGGERS)
