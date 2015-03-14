# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

if not dj_database_url.config():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DEPLOY_MODE = "development"
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'development.sqlite3'),
        }
    }
    DOMAIN_NAME = "http://127.0.0.1:8000"
    MEDIA_ROOT = "%s/media/"%BASE_DIR
    MEDIA_URL = "%s/media/"%DOMAIN_NAME
    STATIC_ROOT = "%s/static/"%BASE_DIR
    STATIC_URL = "%s/static/"%DOMAIN_NAME
    STATICFILES_DIRS = (
        "%s/frontend/assets/"%BASE_DIR,
    )
    WSGI_APPLICATION = 'TAPP.wsgi.application'
else:
    DEBUG = False
    DATABASES = {}
    DATABASES['default'] =  dj_database_url.config()
    DEPLOY_MODE = "production"
    DOMAIN_NAME = ""
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = "%s/static/"%BASE_DIR
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        "%s/frontend/assets/"%BASE_DIR,
    )

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e&uv+ap&vys(&6fniejv&#)a(zq$kpxet=p!6++a9ih&!=bt4@'

# SECURITY WARNING: don't run with debug turned on in production!
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'backend',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TAPP.urls'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# URLs
LOGIN_REDIRECT_URL = '/profile'
LOGIN_URL = '/login'

SITE_ID = 1

TEMPLATE_DIRS = (
    '%s/frontend/templates'%BASE_DIR,
)

########## ALLAUTH ##############
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.contrib.messages.context_processors.messages",
# )
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.contrib.messages.context_processors.messages",
#     # Required by allauth template tags
#     "django.core.context_processors.request",
#     # allauth specific context processors
#     "allauth.account.context_processors.account",
#     "allauth.socialaccount.context_processors.socialaccount",
# )
#
# AUTHENTICATION_BACKENDS = (
#
#     # Needed to login by username in Django admin, regardless of `allauth`
#     "django.contrib.auth.backends.ModelBackend",
#     # `allauth` specific authentication methods, such as login by e-mail
#     "allauth.account.auth_backends.AuthenticationBackend",
# )
#
# SOCIALACCOUNT_QUERY_EMAIL = True
# SOCIALACCOUNT_PROVIDERS = {
#     'facebook': {
#         'SCOPE': ['email', 'publish_stream'],
#         'METHOD': 'js_sdk'
#     }
# }
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
