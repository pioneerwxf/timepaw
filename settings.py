DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/Wangxianfeng/www/djangoproject/data/timepaw.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = '/Users/Wangxianfeng/www/timepaw/media/'

MEDIA_URL = 'http://127.0.0.1:8000/media/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '/Users/Wangxianfeng/www/timepaw/static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
    '/Users/Wangxianfeng/www/timepaw/templates',
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

import djcelery
djcelery.setup_loader()

BROKER_HOST = "git.timepaw.com"
BROKER_PORT = 5672
BROKER_USER = "timepaw_test"
BROKER_PASSWORD = "timepaw_test"
BROKER_VHOST = "test_timepaw_local_2"
