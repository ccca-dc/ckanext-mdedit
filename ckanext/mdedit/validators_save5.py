import json
import datetime
import re
import ckan.lib.helpers as h
from itertools import count
import ast
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _


OneOf = get_validator('OneOf')
ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')

def mdedit_contains(key, data, errors, context):
    """
    Turn list into string; for special field "contains"
    (otherwise we wont get the individual items properly!
    """
    print "***************** Anja********** validate"


    cf = data[key]

    if not cf:
        return

    cs = ""

    # Attention: do not change!
    # or change to same value in json-schema-file
    str_sep = "#"

    # check if str_sep already present: do not do it two times ...

    if type (cf) is not list:
        if cf.find(str_sep) > -1:
            return

    for  x in  cf:
        #cs += str(x)
        cs +=  x
        cs += str_sep

    print cs

    #remove last comma
    data[key] = cs.strip(str_sep)
