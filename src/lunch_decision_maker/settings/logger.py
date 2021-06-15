import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG'),
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
