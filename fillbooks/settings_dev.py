"""
Django settings for fillbooks project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)
HOME_DIR = str(Path.home())

rel_base = lambda *args: os.path.join(BASE_DIR, *args)
rel_home = lambda *args: os.path.join(HOME_DIR, *args)

BD_DIR = "/home/dimadev/fillbooks/db"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i___+56-k$)5o_tl+l$j++fgp2^e1&wi%7qv#_#ihg+$%5km+8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dev.dimankab.fvds.ru', 'dev2.dimankab.fvds.ru']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'main',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fillbooks.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'fillbooks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BD_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = rel_home('media')
COMPRESS_ROOT = rel_home('media')
STATIC_ROOT = rel_home('media', 'static')
MEDIA_URL = '/m/'
STATIC_URL = '/m/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            rel_base('templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.debug',
                # 'django.template.context_processors.tz',
                # 'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

# Django compressor
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True
COMPRESS_URL = MEDIA_URL
COMPRESS_CSSTIDY_BINARY = '/home/sammy/fillbooks/media/CACHE/css'
COMPRESS_CSSTIDY_ARGUMENTS = '--template=highest --sort_properties=false --sort_selectors=false --merge_selectors=1'


COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.datauri.CssDataUriFilter', # 'compressor.filters.csstidy.CSSTidyFilter',
                         'compressor.filters.yui.YUICSSFilter']
COMPRESS_YUI_BINARY = 'java -jar /usr/share/yui-compressor/yui-compressor.jar'

COMPRESS_PRECOMPILERS = (
    ('text/less', '/usr/bin/lessc {infile} {outfile}'),
    #('text/coffeescript', '/home/portal/bin/node /home/portal/node_modules/.bin/coffee --compile --stdio')
) 

