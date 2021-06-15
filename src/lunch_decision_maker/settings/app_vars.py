import os

# django vars
AUTH_USER_MODEL = 'user.User'
ROOT_URLCONF = 'lunch_decision_maker.urls'
WSGI_APPLICATION = 'lunch_decision_maker.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = False
STATIC_URL = '/static/'

# env
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))

REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 8))

AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')

APP_ENV = os.environ.get('APP_ENV')
