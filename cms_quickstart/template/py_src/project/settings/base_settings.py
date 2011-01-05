# -*- coding: utf-8 -*-
from base_cms import *
from base_paths import *
from base_i18n import *

DEBUG = %(dev)s
DEBUG_PROPAGATE_EXCEPTIONS = False
TEMPLATE_DEBUG = DEBUG

PREPEND_WWW = False
FORCE_SCRIPT_NAME = ''

USE_ETAGS = False

INTERNAL_IPS = ['127.0.0.1',]

LOGIN_URL = '/login/'

# DATABASE SETTINGS
DATABASES = {
   'default': {
       'ENGINE': '%(database_engine)s',
       'HOST': '%(database_host)s',
       'NAME': '%(database_name)s',
       'USER': '%(database_user)s',
       'PASSWORD': '%(database_password)s',
       'PORT': '%(database_port)s',
   },
}

TIME_ZONE = None

SITE_ID = 1

USE_I18N = %(i18n)s

USE_L10N = %(l10n)s

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '%(secret_key)s'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
]

ROOT_URLCONF = 'project.urls'


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    # standard plugins
    'cms.plugins.flash',
    'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.text',
    'cms.plugins.twitter',
    'cmsplugin_filer_video',
    'cmsplugin_filer_file',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',

    # standard apps
    'appmedia',
    'cms',
    'filer',
    'menus',
    'mptt',
    'south',
    'tinymce',
    %(reversion_app)s
    
    # custom apps
    'project',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "cms.context_processors.media",
]