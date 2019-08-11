from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_age(value):
    if value < 1 or value > 120:
        raise ValidationError(_('%(value)s is not a valid age'),
                              params={'value', value})


def validate_school_years(value):
    if value < 0 or value > 30:
        raise ValidationError(_('%(value)s is not a valid number of years of schooling'),
                              params={'value', value})

def validate_onset_age(value):
    if value < 3 or value > 81:
        raise ValidationError(_('%(value)s is not a valid age for onset of psychosis'),
                              params={'value', value})

def validate_ill_duration(value):
    if value < 3 or value > 81:
        raise ValidationError(_('%(value)s is not a valid age for illness duration in years'),
                              params={'value', value})

def validate_number_hosp(value):
    if value < 3 or value > 81: # TODO
        raise ValidationError(_('%(value)s is not a valid age for number of hospitalisations'),
                              params={'value', value})

def validate_manic_count(value):
    if value < 0 or value > 7:
        raise ValidationError(_('%(value)s is not a valid count for DSMIV manic symptoms (0-7)'),
                              params={'value', value})