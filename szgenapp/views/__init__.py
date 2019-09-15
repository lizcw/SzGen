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
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': settings.LOG_FILE
        }
    },
    'loggers': {
        '': {
            'level': settings.LOG_LEVEL,
            'handlers': ['console', 'file']
        },
        'django.db.backends': {
            'level': settings.LOG_DB_LEVEL,
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)
