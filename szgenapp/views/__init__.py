from .studies import Study, StudyDelete, StudyCreate, StudyDetail, StudyUpdate, StudyForm, STATUS_CHOICES
from .participants import StudyParticipant, StudyParticipantAdd, StudyParticipantCreate, StudyParticipantDelete, StudyParticipantDetail, StudyParticipantList, StudyParticipantRemove, StudyParticipantUpdate
from .datasets import DatasetCreate, DatasetDelete, DatasetDetail, DatasetFileCreate, DatasetFileList, DatasetFileUpdate, DatasetList, DatasetParticipantList, DatasetParticipantUpdate, DatasetRowCreate, DatasetUpdate
from .samples import SampleDelete, SampleType, SampleDetail, SampleList, SampleParticipantCreate, SampleUpdate, ShipmentCreate, ShipmentDelete, ShipmentUpdate, SubSampleCreate, SubSampleDelete, SubSampleList, SubSampleUpdate, HarvestSampleCreate, HarvestSampleDelete, HarvestSampleUpdate, TransformSampleCreate, TransformSampleDelete, TransformSampleUpdate, QCCreate, QCDelete, QCUpdate
from .clinical import Clinical, ClinicalCreate, ClinicalDelete, ClinicalDemographicCreate, ClinicalDemographicList, ClinicalDemographicUpdate, ClinicalDetail, ClinicalDiagnosisCreate, ClinicalDiagnosisList, ClinicalDiagnosisUpdate, ClinicalList, ClinicalMedicalCreate, ClinicalMedicalList, ClinicalMedicalUpdate, ClinicalSymptomsBehaviourCreate, ClinicalSymptomsBehaviourList, ClinicalSymptomsBehaviourUpdate, ClinicalSymptomsDelusionCreate, ClinicalSymptomsDelusionList, ClinicalSymptomsDelusionUpdate, ClinicalSymptomsDepressionCreate, ClinicalSymptomsDepressionList, ClinicalSymptomsDepressionUpdate, ClinicalSymptomsGeneralCreate, ClinicalSymptomsGeneralList, ClinicalSymptomsGeneralUpdate, ClinicalSymptomsHallucinationCreate, ClinicalSymptomsHallucinationList, ClinicalSymptomsHallucinationUpdate, ClinicalSymptomsManiaCreate, ClinicalSymptomsManiaList, ClinicalSymptomsManiaUpdate
from .document import Document, DocumentCreate, DocumentDelete, DocumentDetail, DocumentImport, DocumentList, DocumentUpdate, DocumentFilter, DocumentForm, DocumentTable
from .help import HelpDetail
from .auth import LoginView, LogoutView, locked_out, csrf_failure
# Set up Logging
import logging.config
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
