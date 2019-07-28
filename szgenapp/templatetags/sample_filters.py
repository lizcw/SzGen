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