import json
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df
import ckanext.mdedit.helpers as helpers
from itertools import count
from ckan.plugins.toolkit import get_validator, UnknownValidator, missing, Invalid, _
from ckanext.scheming.validation import scheming_validator

from ckanext.mdedit.helpers import parse_json

import ckan.plugins.toolkit as tk


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
        elif len(data.get(('relations',), [])) > 0:
            data_dict['relations'] = json.loads(data[('relations',)])

        pkg_for_versioning = data_dict

        if len(data_dict.get('relations', [])) > 0:
            parent_ids = [element['id'] for element in data_dict['relations'] if element['relation'] == 'is_part_of']

            if len(parent_ids) > 0:
                pkg_for_versioning = tk.get_action('package_show')(context, {'id': parent_ids[0]})

        name = data[key]
        version_number = str(get_version_number(pkg_for_versioning)).zfill(2)

        if not name.endswith('-v' + version_number):
            data[key] = name + '-v' + version_number

        context['ignore_capacity_check'] = True
        # newer versions use 'include_private': True in package_search
        search_results = tk.get_action('package_search')(context, {'rows': 1000, 'fq': 'name:"%s"' % (data[key]), 'include_versions': True})

        if search_results['count'] > 0:
            if data.get(('id',), '') != search_results['results'][0]['id']:
                errors[key].append(_('That URL is already in use.'))

    return validator


@scheming_validator
def readonly_subset_fields(field, schema, is_dict=False):
    def validator(key, data, errors, context):
        """
        validator makes sure that some fields of subsets
        cannot be changed
        """
        #
        # if errors[key]:
        #     return

        if data.get(('id',), '') != '':
            data, errors = _readonly_subset_fields(key, data, errors, context, field['field_name'])

    return validator


@scheming_validator
def readonly_subset_fields_dicts(field, schema, is_dict=False):
    def validator(key, data, errors, context):
        """
        validator makes sure that some fields of subsets
        cannot be changed
        """
        #
        # if errors[key]:
        #     return

        if data.get(('id',), '') != '':
            print(data[key])

            import ast
            try:
                data[key] = ast.literal_eval(data.get(key, ''))
            except:
                pass

            print("************")
            print(parse_json(data[key]))
            print(data[key])
            old_package = tk.get_action('package_show')(context, {'id': data[('id',)]})
            print("*****************")
            print(old_package.get(field['field_name'], ''))
            print(json.dumps(old_package.get(field['field_name'], '')))

            data, errors = _readonly_subset_fields(key, data, errors, context, field['field_name'])

    return validator


def _readonly_subset_fields(key, data, errors, context, field_name):
    old_package = tk.get_action('package_show')(context, {'id': data[('id',)]})
    if old_package.get(field_name, '') != data.get(key, ''):
        if data.get(('relations',), '') != '':
            relations = json.loads(data[('relations',)])

            if len(relations) > 0:
                parent_ids = [element['id'] for element in relations if element['relation'] == 'is_part_of']

                if len(parent_ids) > 0:
                    errors[key].append(_('Subsets cannot change this field'))

    return data, errors
