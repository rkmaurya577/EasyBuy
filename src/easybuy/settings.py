"""
Django settings for easybuy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2_=0yfh^cl*188(*%f90qu3sf*%wk!nqe$blbzjg9q)ke1%0ov'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_FROM_EMAIL = "yourid@gmail.com"

try:
    from .email_settings import host,user,password
    EMAIL_HOST = host #"smtp.gmail.com"  #sendgrid  for transactional email
    EMAIL_HOST_USER = user #"yourid@gmail.com"
    EMAIL_HOST_PASSWORD = password #"password"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
except:
    pass

if DEBUG:
    SITE_URL = "http://127.0.0.1:8000"
if not DEBUG:
    SITE_URL = "abc.com"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'accounts',
    'carts',
    'marketing',
    'orders',
    'products',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'marketing.middleware.DisplayMarketing',
)

ROOT_URLCONF = 'easybuy.urls'

WSGI_APPLICATION = 'easybuy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MARKETING_HOURS_OFFSET = 3
MARKETING_SECONDS_OFFSET = 0

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "django.core.context_processors.request",
    )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static","media")
# MEDIA_ROOT = "/media/squad/MAURYA/easybuy/easybuy/static/media/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static","static_root")

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static","static_files"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    )

STRIPE_SECRET_KEY = "sk_test_3B4nJzYss9X1KvaYvLeyhf1W"
STRIPE_PUBLISHABLE_KEY = "pk_test_AvgFANgowGmnKt1e6CSY4IJG"

    
