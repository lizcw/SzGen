from django.core.exceptions import ValidationError

"""
What the docs don't say is that the code must be unique from django-forms - don't use 'invalid'
"""

def validate_age(value):
    if int(value) < 1 or int(value) > 120:
        raise ValidationError(message='Value is not a valid age (0-120)',
                              code='age_invalid')


def validate_school_years(value):
    if int(value) < 0 or int(value) > 30:
        raise ValidationError(message='Value is not a valid number of years of schooling (0-30)',
                              code='school_years_invalid')

def validate_onset_age(value):
    if int(value) < 3 or int(value) > 81:
        raise ValidationError(message='Value is not a valid age for onset of psychosis (3-81)',
                              code='onset_age_invalid')

def validate_ill_duration(value):
    if int(value) < 0 or int(value) > 100:
        raise ValidationError(message='Value is not a valid age for illness duration in years(0-100)',
                              code='ill_duration_invalid',)

def validate_number_hosp(value):
    if int(value) < 0 or int(value) > 1000:
        raise ValidationError(message='Value is not a valid number of hospitalisations (0-1000)',
                              code='number_hosp_invalid')

def validate_manic_count(value):
    if int(value) < 0 or int(value) > 7:
        raise ValidationError(message='Value is not a valid count for DSMIV manic symptoms (0-7)',
                              code='manic_count_invalid')

def validate_depression_count(value):
    if int(value) < 0 or int(value) > 9:
        raise ValidationError(message='Value is not a valid count for DSMIV depressive symptoms (0-9)',
                              code='depression_count_invalid')