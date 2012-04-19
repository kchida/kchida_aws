# -*- coding: utf-8 -*-
# Django settings for kchida_aws project.

from os.path import abspath, basename, dirname, join
import sys

PROJECT_PATH = abspath(dirname(dirname(__file__)))
PROJECT_NAME = basename(PROJECT_PATH)
sys.path.append(PROJECT_PATH)

# TODO: Automate detection of development vs production server..
# TODO: Automate detection of external static library files (i.e. jquery, modernizr, jqueryui)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# Turn on django_compressor independent of DEBUG setting above.
#COMPRESS_ENABLED = True
# Below should only apply for DEBUG = True
COMPRESS_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ADMINS = (
    ('Ken Chida', 'ken.chida@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/kchida/workspace/kchida_aws/kchida_aws.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_NAME = 'Ken Chida Website'
SITE_COPYRIGHT = 'copyright'
SITE_ID = 1

DISQUS_SHORTNAME = 'kchida'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(PROJECT_PATH, '_collected_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_DIRS = (join(PROJECT_PATH, 'static'),) + STATICFILES_DIRS

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'chg%44!%6x43atnzbet7p)bm1dleo(k9+seo9(p53f*8g^2^mv'

############
# TEMPLATE #
############
# List of hard-coded template directories.
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Don't forget to use absolute paths, not relative paths.
)
# Adds main template directory.
TEMPLATE_DIRS = (join(PROJECT_PATH, 'templates'),) + TEMPLATE_DIRS

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_type_backends',
    'apps.minicms.context_processors.cms',
    'apps.user.context_processors.login_reg',
)

##############
# MIDDLEWARE #
##############
# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'apps.autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.urlrouter.middleware.URLRouterFallbackMiddleware',

)

###############
# URL ROUTING #
###############
ROOT_URLCONF = 'kchida_aws.urls'

URL_ROUTE_HANDLERS = (
    'apps.minicms.urlroutes.PageRoutes',
    'apps.blog.urlroutes.BlogRoutes',
    'apps.blog.urlroutes.BlogPostRoutes',
    'apps.redirects.urlroutes.RedirectRoutes',
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'kchida_aws.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'compressor',
    'social_auth',
    'apps.disqus',
    'apps.urlrouter',
    'apps.minicms',
    'apps.blog',
    'apps.user',
    'apps.autoload',
)

# Restructured Text
REST_BACKENDS = (
    'apps.minicms.markup_highlight',
    'apps.blog.markup_posts',
)
##################
# AUTHENTICATION #
##################

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Main URL that allows people to log in. Modal window is used on main screen.
# TODO: Create a fallback for clients with JS turned off.
LOGIN_URL = '/'
LOGOUT_URL = '/logout/'
# Redirect URL directly following login.
LOGIN_REDIRECT_URL = '/'#/logged-in/'
LOGIN_ERROR_URL = '/login-error/'
# The number of days a password reset link is valid for
PASSWORD_RESET_TIMEOUT_DAYS = 3

###### Begin: Django-social-auth settings #######
SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'google-oauth', 'twitter',)

# TODO: Store key outside of public BitBucket repo
TWITTER_CONSUMER_KEY = 'aNHGCuBL3eQLiqZqvxQiaQ'
TWITTER_CONSUMER_SECRET = 'qjDVV0tewGFn8jBEGjAAwsZM9RPYgbp9K6nsBLnsysU'
GOOGLE_CONSUMER_KEY = ''
GOOGLE_CONSUMER_SECRET = ''
#GOOGLE_OAUTH2_CLIENT_ID = ''
#GOOGLE_OAUTH2_CLIENT_SECRET = ''

SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME = 'socialauth_user'
# Make sure all social auth logins are also registered.
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/register/'
# Request new users to create username and password, and/or associate accounts.
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/register/'
# Redirect back to 'associate-begin' URL. If user is done, they can exit.
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/user-account/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/user-account/'

#SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

###### End: Django-social-auth settings #####


AUTH_PROFILE_MODULE = 'apps.user.models.MyProfile'

###########
#  EMAIL  #
###########
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

###########
# LOGGING #
###########
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}

try:
    from local_settings import *
except:
    pass
