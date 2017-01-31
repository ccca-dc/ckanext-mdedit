import json
import datetime
import re
import ckan.lib.helpers as h
from itertools import count
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _


def mdedit_contains(key, data, errors, context):

    """
    Accept  values as a list of contact info
    convert to a json list for storage:

    1. a list of strings, eg.:

       ["Vorname Nachname", "Institut Blabal", ...]

    2. a single string for  a single:

       "Name"

     (Addpated from scheming multiple choice)
    """
    #if errors[key]:
    #    return

    print "***************** Anja********** mdedit_contains validator"
    print data[key]

    value = data[key]

    if value is not missing:
        if isinstance(value, basestring):
            value = [value]
        elif not isinstance(value, list):
            errors[key].append(_('expecting contact info list'))
            return
    else:
        value = []

    if not errors[key]:
        data[key] = json.dumps(value)

    print errors[key]
    print data[key]
