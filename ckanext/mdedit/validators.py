import json
import datetime
import re
import ckan.lib.helpers as h
from itertools import count
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _


def mdedit_contains_k(key, data, errors, context):

    """
    Accept  values as a list of contact info
    convert to a json list for storage:

    1. a list of strings, eg.:

       ["Vorname Nachname", "Institut Blabal", ...]

    2. a single string for  a single:

       "Name"

     (Addpated from scheming multiple choice)
    """
    #
    # #print "***************** Anja********** mdedit_contains validator"
    #
    # value = data[key]
    #
    # #print value
    # #print type(value)
    #
    # if value is not missing:
    #     if not isinstance(value, list):
    #         #errors[key].append(_('expecting contact info list'))
    #         return
    entered_list = data[key]
    if type(entered_list) == str or type(entered_list) == unicode:
        return
    elif type(entered_list) == list:
        if type(entered_list[0]) == unicode or type(entered_list[0]) == str:
            contact_dicts = []
            for index, value in enumerate(entered_list):
                print(value, index)
                if (index + 1) % 4 == 0 and index != 0:
                    contact_dicts.append({'name': entered_list[index-3], 'department': entered_list[index-2], 'email': entered_list[index-1], 'role': value})
    else:
        contact_dicts = entered_list

    data[key] = json.dumps(contact_dicts)
