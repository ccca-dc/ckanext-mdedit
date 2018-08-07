import json
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df
import ckanext.mdedit.helpers as helpers
from itertools import count
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _
from ckanext.scheming.validation import scheming_validator

from ckanext.mdedit.helpers import parse_json

import ckan.plugins.toolkit as tk
import ckan.authz as authz


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

    value = data[key]

    if value is not missing:
        if not isinstance(value, list):
            #errors[key].append(_('expecting contact info list'))
            return
    else:
        value = []

    if not errors[key]:
        data[key] = json.dumps(value)


@scheming_validator
def multiple_text(field, schema):
    """
    Accept zero or more values as a list and convert
    to a json list for storage:
    1. a list of strings, eg.:
       ["somevalue a", "somevalue -b"]
    2. a single string for single item selection in form submissions:
       "somevalue-a"
    """
    def validator(key, data, errors, context):
        # if there was an error before calling our validator
        # don't bother with our validation
        # if errors[key]:
        #     return

        value = data.get(key, missing)
        if value is not missing:
            if isinstance(value, basestring):
                value = [value]
            elif not isinstance(value, list):
                errors[key].append(
                    _('Expecting list of strings, got "%s"') % str(value)
                )
                return
        else:
            value = []

        if not errors[key]:
            data[key] = json.dumps(value)

    return validator


@scheming_validator
def list_of_dicts(field, schema):
    def validator(key, data, errors, context):
        # if there was an error before calling our validator
        # don't bother with our validation

        if errors[key]:
            return

        try:
            data_dict = df.unflatten(data[('__junk',)])
            value = data_dict[key[0]]
            if value is not missing:
                if isinstance(value, basestring):
                    value = [value]
                elif not isinstance(value, list):
                    errors[key].append(
                        _('Expecting list of strings, got "%s"') % str(value)
                    )
                    return
            else:
                value = []


            if not errors[key]:
                data[key] = json.dumps(value)

            del data_dict[key[0]]
            data[('__junk',)] = df.flatten_dict(data_dict)
        except KeyError:
            # Empty lists have to be treated here
            try:
                if not errors[key] and len(data[key]) == 0:
                    value = []
                    data[key] = json.dumps(value)
            except:
                pass


    return validator


def multiple_text_output(value):
    """
    Return stored json representation as a list
    """
    return parse_json(value, default_value=[value])


@scheming_validator
def version_to_name(field, schema):
    def validator(key, data, errors, context):
        """
        validator makes sure that packages have their version number
        at the end of their name
        """

        from ckanext.resourceversions.helpers import get_version_number

        data_dict = dict()
        if ('__junk',) in data:
            data_dict = df.unflatten(data[('__junk',)])
        elif data.get(('relations',), '') is not missing and len(data.get(('relations',), [])) > 0:
            data_dict['relations'] = json.loads(data[('relations',)])

        pkg_for_versioning = data_dict

        if 'relations' in data_dict:
            rel_dict = data_dict['relations']
        else:
            rel_dict = None

        if type(rel_dict) == list and len(rel_dict) > 0:
            parent_ids = [element['id'] for element in rel_dict if element['relation'] == 'is_part_of']

            if len(parent_ids) > 0:
                # copy context otherwise the context contains the parent package and the next validator has a problem
                context_copy = context.copy()
                pkg_for_versioning = tk.get_action('package_show')(context_copy, {'id': parent_ids[0]})

        name = data[key]
        version_number = str(get_version_number(pkg_for_versioning)).zfill(2)

        if not name.endswith('-v' + version_number):
            data[key] = name + '-v' + version_number

    return validator


@scheming_validator
def readonly_subset_fields(field, schema, is_dict=False):
    def validator(key, data, errors, context):
        """
        validator makes sure that some fields of subsets
        cannot be changed
        """
        user = context.get('user')

        if not authz.is_sysadmin(user) and data.get(('id',), '') is not missing and data.get(('id',), '') not in ('', None):
            data, errors = _readonly_subset_fields(data, key, data[key], errors, context, field['field_name'])

    return validator


@scheming_validator
def readonly_subset_fields_dicts(field, schema, is_dict=False):
    def validator(key, data, errors, context):
        """
        validator makes sure that some dict fields of subsets
        cannot be changed
        """
        user = context.get('user')

        if not authz.is_sysadmin(user) and data.get(('id',), '') is not missing and data.get(('id',), '') not in ('', None):
            try:
                import ast
                new_value = ast.literal_eval(data[key])
            except:
                new_value = data[key]

            data, errors = _readonly_subset_fields(data, key, new_value, errors, context, field['field_name'])

    return validator


def _readonly_subset_fields(data, key, new_value, errors, context, field_name):

    old_package = tk.get_action('package_show')(context, {'id': data[('id',)]})

    if old_package.get(field_name, '') != new_value:

        relations = old_package.get('relations', [])

        if len(relations) > 0:
            parent_ids = [element['id'] for element in relations if element['relation'] == 'is_part_of']

            if len(parent_ids) > 0:
                #Anja, 24.7.18: Check if only a new field was added
                # This might happen, if we introduce new fields or
                # the netcdf originally did not have a corresponding value
                result =_check_new_field(old_package.get(field_name, ''), new_value)
                if ( result != ''):
                    errors[key].append(_('Subsets cannot change this field {:s}').format(result))
                #     print "Field_Name (FAILED): "
                #     print field_name
                #     print "************** mdedit new_value"
                #     print json.dumps (new_value, indent=4)
                #     print "**************  old_value"
                #     print json.dumps (old_package.get(field_name, ''), indent=4)
                # print "Field_Name (OK): "
                # print field_name
                # print "************** mdedit new_value"
                # print json.dumps (new_value, indent=4)
                # print "**************  old_value"
                # print json.dumps (old_package.get(field_name, ''), indent=4)
    return data, errors

def _check_new_field(old_list, new_list):
    # Check if we just have a new field as difference
    if not isinstance(old_list, list):
        return False
    if not isinstance(new_list, list):
        return False

    for d_new in new_list:

        d_old = _find_dict_in_list(d_new, old_list)

        if d_old != None:
            if d_old == d_new:
                return ''
            #Check the difference
            diff_dict = { k : d_new[k] for k in set(d_new) - set(d_old) }

            # Allowed are only empty values!

            for k,v in diff_dict.iteritems():
                if v != '':
                    return v

            return ''

        else:
            return d_new

def _find_dict_in_list(specific_dict, dict_list):
    # specific_dict might have more fields than the
    # corresponding element in the dict_list itself.
    # But the rest of the fields should be identical



    candidate ={}

    for d in dict_list:
        for kl,vl in d.iteritems():
            if kl in specific_dict and specific_dict[kl] == vl:
                candidate = d
                continue
            else:
                candidate = {}
                break

        if candidate:
            return candidate


    return None
