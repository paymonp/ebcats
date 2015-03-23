"""
Django settings for ebcats project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(a5va*(8fx^7ol6^1nr5#&5v9=3oozk3@kt!ddu9)s1v6knzpy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'compressor',
    'ebcatsapp',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ebcats.urls'

WSGI_APPLICATION = 'ebcats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'ebcatsapp/static/'
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    #creates absolute urls from relative ones
    'compressor.filters.css_default.CssAbsoluteFilter',
    #css minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/scss', 'sass --scss {infile} {outfile}'),
)

EVENTBRITE_API_TOKEN = 'A5F6TPUDWWEP7CSC4SQX'

"""
Settings for MemCachier (memcached for Heroku)
From https://github.com/memcachier/examples-django2

*Modified to fit our needs:
24 hour timeout (not sure how often events get updated) and infinite max entries
"""
## MemCachier Settings
## ===================
def get_cache():
  # We do this complicated cache defenition so that on a local machine (where
  # MEMCACHIER_SERVERS won't be defined), the try fails and so we use the
  # inbuilt local memory cache of django.
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'BINARY': True,
        'TIMEOUT': 86400,
        'OPTIONS': {
            'no_block': True,
            'tcp_nodelay': True,
            'tcp_keepalive': True,
            'remove_failed': 4,
            'retry_timeout': 2,
            '_poll_timeout': 2000,
            'MAX_ENTRIES': 10e9
        }
      }
    }
  except:
    # Use django local development cache (for local development).
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 86400,
        'OPTIONS': {
            'MAX_ENTRIES': 10e9
        }
      }
    }

CACHES = get_cache()