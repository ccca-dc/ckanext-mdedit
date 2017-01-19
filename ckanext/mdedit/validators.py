import json
import datetime
import re
import ckan.lib.helpers as h
from itertools import count
from ckanext.scheming import helpers as hs

from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _


OneOf = get_validator('OneOf')
ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')

def mdedit_contains(key, data, errors, context):
    """
    Turn list into string; for special field "contains"
    (lists run per default into tag_string_validator and get manipulated - we need to omit this)
    """
    print "***************** Anja********** validate"


    print  key
    print data
    print context

    pkg = context.get('package_extra')
    print "****package:"
    print pkg
    print context.get ('contact_info')
    print data[key]
    print type(data[key])

    cf = data[key]

    if not cf:
        return

    cs = ""

    for x in cf:
        cs += str(x)
        cs += "#"

    # remove last comma
    data[key] = cs.strip('#')

    print data[key]
    print type(data[key])
