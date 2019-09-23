from django import template

register = template.Library()

@register.filter(name='filtersamples')
def filtersamples(value, arg):
    """
    Filter subsamples set by type
    :param value: subsamples_set
    :param arg: string type
    :return: filtered set
    """
    return value.filter(sample_type=arg)

@register.filter(name='countsamples')
def countsamples(value, arg):
    """
    Count subsamples set by type
    :param value: subsamples_set
    :param arg: string type
    :return: number
    """
    return value.filter(sample_type=arg).count()

@register.filter(name='failpass')
def failpass(value):
    """
    Provide 'failed' if true or 'passed' if false
    :param value: boolean
    :return:
    """
    if value:
        return 'fail'
    else:
        return 'pass'

@register.filter(name='passfail')
def passfail(value):
    """
    Provide 'failed' if false or 'passed' if true #TODO Fix these inconsistent fields
    :param value: boolean
    :return:
    """
    if not value:
        return 'fail'
    else:
        return 'pass'

@register.filter(name='fieldvalue')
def fieldvalue(value, fieldlist):
    """
    Get lookup value from values list (dict)
    :param value: fieldname value for lookup
    :param fieldlist: dict() for lookup
    :return:
    """
    return fieldlist[value]
