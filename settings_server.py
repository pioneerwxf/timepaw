# this file is for server settings
import os
import json
import djcelery
with open('/home/dotcloud/environment.json') as f:
    dotcloud_env = json.load(f)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'template1',                      # Or path to database file if using sqlite3.
        'USER': dotcloud_env['DOTCLOUD_DB_SQL_LOGIN'],                      # Not used with sqlite3.
        'PASSWORD': dotcloud_env['DOTCLOUD_DB_SQL_PASSWORD'],                  # Not used with sqlite3.
        'HOST': dotcloud_env['DOTCLOUD_DB_SQL_HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': int(dotcloud_env['DOTCLOUD_DB_SQL_PORT']),                      # Set to empty string for default. Not used with sqlite3.
    }
}

djcelery.setup_loader()
BROKER_HOST = 'git.timepaw.com'
BROKER_PORT = 5672
BROKER_USER = 'timepaw_test'
BROKER_PASSWORD = 'timepaw_test'
BROKER_VHOST = 'test_timepaw'

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'topic',
        'binding_key': 'tasks.#'
    }
}

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = '/home/dotcloud/data/media/'

MEDIA_URL = 'http://www.timepaw.com/media/'

STATIC_ROOT = '/home/dotcloud/data/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '/home/dotcloud/current/timepaw/static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '&pn6*#gz(178-6q1!j47r$9#a+zndn+chjm3g#f8t0sn)bg&h4'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'timepaw.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'timepaw.profiles',
    'timepaw.paws',
    'timepaw.datasources',
    'timepaw.activekeys',
)
