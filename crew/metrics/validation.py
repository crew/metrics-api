from . import api


def check_float(obj, name='obj'):
    if not obj:
        raise api.ValidationError('%s cannot be empty.' % name)
    if not type(obj) == float:
        raise api.ValidationError('%s has to be a float.' % name)


def check_int(obj, name='obj'):
    if not obj:
        raise api.ValidationError('%s cannot be empty.' % name)
    if not type(obj) == int:
        raise api.ValidationError('%s has to be a int.' % name)


def check_list(obj, check_type=None, name='obj'):
    if not type(obj) in (list, tuple):
        raise api.ValidationError('%s has to be a list or a tuple.' % name)
    if check_type:
        for x in obj:
            if not check_type == type(x):
                raise api.ValidationError('%s needs to contains %s' %
                    (name, str(check_type)))
