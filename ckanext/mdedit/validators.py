import json
import ckan.lib.helpers as h
import ckanext.mdedit.helpers as helpers
from itertools import count
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _
from ckanext.scheming.validation import scheming_validator


@scheming_validator
def mdedit_contains_k(field, schema):

    def validator(key, data, errors, context):

        """
        Accept  values as a list of contact info
        convert to a json list for storage:

        1. a list of strings, eg.:

           ["Vorname Nachname", "Institut Blabal", ...]

        2. a single string for  a single:

           "Name"

         (Adapted from scheming multiple choice)
        """

        # if there was an error before calling our validator
        # don't bother with our validation
        if errors[key]:
                return

        value = data.get(key)

        if value is not missing:
            if not isinstance(value, (list, str, unicode)):
                errors[key].append(_('expecting list of strings or dicts in list as string'))
                return
        else:
            return

        labels = helpers.mdedit_get_contain_labels(field)

        # type is string if called from api
        if isinstance(value, (str, unicode)):
            try:
                value = json.loads(value.decode('utf-8'))

                if type(value) != list:
                    errors[key].append(_('expecting list of strings or dicts in list as string'))
                else:
                    for contact in value:
                        if type(contact) == dict:
                            labels = [x.lower() for x in labels]
                            if not all(k in contact for k in labels):
                                errors[key].append(_('missing key(s)'))
                        else:
                            errors[key].append(_('expecting list of strings or dicts in list as string'))
            except:
                errors[key].append(_('expecting list of strings or dicts in list as string'))
            return
        else:
            num_contains = int(field['contains'])

            if all(isinstance(x, (str, unicode)) for x in value):
                contact_dicts = []
                for index, val in enumerate(value):
                    # converting every 4 values to dict
                    if (index + 1) % num_contains == 0 and index != 0:
                        contact = {}
                        for i in range(num_contains):
                            contact[labels[i].lower()] = value[index-num_contains+1+i]
                        contact_dicts.append(contact)
            else:
                errors[key].append(_('expecting list of strings or dicts in list as string'))
                return

        data[key] = json.dumps(contact_dicts)

    return validator


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

    #print "***************** Anja********** mdedit_contains validator"

    value = data[key]

    #print value
    #print type(value)

    if value is not missing:
        if not isinstance(value, list):
            #errors[key].append(_('expecting contact info list'))
            return
    else:
        value = []

    if not errors[key]:
        data[key] = json.dumps(value)

#    print errors[key]
#    print data[key]
#    print type(data[key])
