from .studies import Study, StudyDelete, StudyCreate, StudyDetail, StudyUpdate, StudyForm, STATUS_CHOICES
from .participants import *
from .datasets import *
from .samples import *
from .clinical import *
from .document import *
from .auth import LoginView, LogoutView, locked_out, csrf_failure

# Set up Logging
import logging
from django.conf import settings


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': settings.LOG_FILE,
            'maxBytes': 1024*1024*5,
            'backupCount': 2
        }
    },
    'loggers': {
        '': {
            'level': settings.LOG_LEVEL,
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'django.db.backends': {
            'level': settings.LOG_DB_LEVEL,
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)
