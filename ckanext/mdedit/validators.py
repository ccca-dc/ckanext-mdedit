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
    (otherwise we wont get the individual items properly!
    """
    #print "***************** Anja********** validate"


    #print  key
    #print data
    #print context

    #pkg = context.get('package_extra')
    #print "****package:"
    #print pkg
    #print context.get ('contact_info')
    #print "************** Before *************"
    #print data[key]
    #print type(data[key])
    #print key
    #print data[u'str_sep']

    cf = data[key]

    if not cf:
        return

    cs = ""
    # Attention: do not change!
    # or change to same value in json-schema-file
    str_sep = "#"
    for x in cf:
        #cs += str(x)
        cs +=  x
        cs += str_sep

    #remove last comma
    data[key] = cs.strip(str_sep)

    #print "************** after (cs) *************"
    #print data[key]
    #print type(data[key])
