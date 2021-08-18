import os

from ._settings import *

INSTALLED_APPS += [
    # Rich text editor
    'ckeditor',
    # This package is used for use tagging system
    'taggit',
    # This package is used for showing location of restaurants
    'mapbox',
    # This package is used for comment system
    'django_comments_xtd',
    'django_comments',
    # Google authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Multi select model for django admin
    'multiselectfield',
    # This package is used for create range of date
    'pandas',

    # Created apps
    'Yummy_site',
    'Yummy.apps.YummyConfig',
    'Blog.apps.BlogConfig',
    'Users.apps.UsersConfig',
    'Menu.apps.MenuConfig',
    'Ordering.apps.OrderingConfig',
]

AUTH_USER_MODEL = 'Users.User'
SITE_ID = 1
LOGIN_URL = '/users/Register/'

# Static settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Yummy', 'static')
]

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'yummy.site.rest@gmail.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = 'pass.Yum.1278'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Message settings
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'error',
    messages.SUCCESS: 'success',
}

#  Mapbox settings
MAPBOX_KEY = 'pk.eyJ1Ijoic2hheWVzdGVoaHMiLCJhIjoiY2twOGZ3dzgyMDN2NTJwbGx5YzA4MTQ5dSJ9.Y1ZpmbLF7CH_SQxr1ixdkw'

# Comment settings
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MODEL = 'Blog.models.CustomComment'
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_XTD_MAX_THREAD_LEVEL = 5
COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'default': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
        'who_can_post': 'user'  # Valid values: 'all', users'
    }
}

# Google authentication settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Default is = 3
ACCOUNT_EMAIL_REQUIRED = True  # Default is = False
ACCOUNT_ADAPTER = "utility.adapter.CustomAccountAdapter"
ACCOUNT_EMAIL_BLACKLIST = ['hosseinshayesteh47.hs@gmail.com']
ACCOUNT_AUTHENTICATION_METHOD = 'email'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
