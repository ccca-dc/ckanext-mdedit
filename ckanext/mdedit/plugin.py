import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import json
import ckanext.mdedit.logic.action as action
import pylons

from ckanext.mdedit import helpers
from ckanext.mdedit import validators as v
ignore_empty = plugins.toolkit.get_validator('ignore_empty')

from ckanext.mdedit.helpers import (
    localize_json_title, get_frequency_name, get_readable_file_size,
    parse_json, dump_json, map_to_valid_format
)


class MdeditPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mdedit')

    # IValidators
    def get_validators(self):
        return {
            'mdedit_contains_k': v.mdedit_contains_k,
            'multiple_text': v.multiple_text,
            'multiple_text_output': v.multiple_text_output,
            'list_of_dicts': v.list_of_dicts,
            'parse_json': parse_json,
            'version_to_name': v.version_to_name,
            'readonly_subset_fields': v.readonly_subset_fields,
            'readonly_subset_fields_dicts': v.readonly_subset_fields_dicts
            }

    # IActions
    def get_actions(self):
        actions = {'package_contact_show': action.package_contact_show}
        return actions

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'mdedit_get_package_name': helpers.mdedit_get_package_name,
            'mdedit_get_name': helpers.mdedit_get_name,
            'mdedit_get_mail': helpers.mdedit_get_mail,
            'mdedit_get_date': helpers.mdedit_get_date,
            'mdedit_parse_date': helpers.mdedit_parse_date,
            'mdedit_get_name_citation': helpers.mdedit_get_name_citation,
            'mdedit_get_contain_values_k': helpers.mdedit_get_contain_values_k,
            'mdedit_get_contain_labels': helpers.mdedit_get_contain_labels,
            'mdedit_get_contain_pholders': helpers.mdedit_get_contain_pholders,
            'mdedit_get_resource_version': helpers.mdedit_get_resource_version,
            'mdedit_get_resource_title': helpers.mdedit_get_resource_title,
            'mdedit_get_package_id': helpers.mdedit_get_package_id,
            'mdedit_get_contact_choices': helpers.mdedit_get_contact_choices,
            'mdedit_get_contact_values': helpers.mdedit_get_contact_values,
            'get_readable_file_size': helpers.get_readable_file_size,
            'get_frequency_name': helpers.get_frequency_name,
            'parse_json': helpers.parse_json,
            'dump_json': helpers.dump_json
            }


class MdeditMasterPlugin(plugins.SingletonPlugin):
    """
    Handles dictionaries in data_dict (pkg_dict).
    """

    def before_view(self, pkg_dict):
        pkg_dict = self._prepare_package_json(pkg_dict)
        return pkg_dict

    def _parse_field(self, key):
        #return False
        return key in 'contact_points' or key in 'specifics' or key in 'variables' or key in 'dimensions' or key in 'relations'


    def _prepare_package_json(self, pkg_dict):
        # parse all json strings in dict
        pkg_dict = self._package_parse_json_strings(pkg_dict)

        # map ckan fields
        pkg_dict = self._package_map_ckan_default_fields(pkg_dict)

        #try:
        #    # Do not change the resulting dict for API requests
        #    path = pylons.request.path
        #    if path.startswith('/api'):
        #        return pkg_dict
        #except TypeError:
        #    # we get here if there is no request (i.e. on the command line)
        #    return pkg_dict

        return pkg_dict


    def _package_parse_json_strings(self, pkg_dict):
        # try to parse all values as JSON
        for key, value in pkg_dict.iteritems():
            if self._parse_field(key):
                pkg_dict[key] = parse_json(value)
        return pkg_dict


    def _package_map_ckan_default_fields(self, pkg_dict):  # noqa
        # Map Maintainer and author from contact_points
        if pkg_dict.get('maintainer') is None:
            try:
                pkg_dict['maintainer'] = pkg_dict['contact_points'][0]['name']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        if pkg_dict.get('maintainer_email') is None:
            try:
                pkg_dict['maintainer_email'] = pkg_dict['contact_points'][0]['email']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        if pkg_dict.get('author') is None:
            try:
                pkg_dict['author'] = pkg_dict['contact_points'][0]['name']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        if pkg_dict.get('author_email') is None:
            try:
                pkg_dict['author_email'] = pkg_dict['contact_points'][0]['email']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        # Map Temporals for DCAT Export
        # TODO Support multiple temporal extents
        if pkg_dict.get('temporal_start') is None:
            try:
                pkg_dict['temporal_start'] = pkg_dict['temporals'][0]['start_date']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        if pkg_dict.get('temporal_end') is None:
            try:
                pkg_dict['temporal_end'] = pkg_dict['temporals'][0]['end_date']  # noqa
            except (KeyError, IndexError, TypeError):
                pass

        return pkg_dict


class MdeditResourcePlugin(MdeditMasterPlugin):
    plugins.implements(plugins.IResourceController, inherit=True)

    # IResourceController
    def before_show(self, res_dict):
        res_dict = super(MdeditResourcePlugin, self).before_view(res_dict)
        # res_dict = self._prepare_resource_format(res_dict)

        # if format could not be mapped and media_type exists use this value
        # if not res_dict.get('format') and res_dict.get('media_type'):
        #     res_dict['format'] = res_dict['media_type'].split('/')[-1]

        return res_dict

    def _ignore_field(self, key):
        return key == 'tracking_summary' or key in 'name' or key in 'description'


class MdeditPackagePlugin(MdeditMasterPlugin):
    plugins.implements(plugins.IPackageController, inherit=True)

    def is_supported_package_type(self, pkg_dict):
        # only package type 'dataset' is supported (not harvesters!)
        try:
            return (pkg_dict['type'] == 'dataset')
        except KeyError:
            return False

    # IPackageController
    def before_view(self, pkg_dict):
        if not self.is_supported_package_type(pkg_dict):
            return pkg_dict

        return super(MdeditPackagePlugin, self).before_view(pkg_dict)

    def after_show(self, context, pkg_dict):
        if not self.is_supported_package_type(pkg_dict):
            return pkg_dict

        pkg_dict = self._package_map_ckan_default_fields(pkg_dict)

        return super(MdeditPackagePlugin, self).before_view(pkg_dict)
        #return pkg_dict

    def before_index(self, search_data):
        if not self.is_supported_package_type(search_data):
            return search_data

        validated_dict = json.loads(search_data['validated_data_dict'])

        variables = []

        # Add any specified variables to search_data
        if u'variables' in validated_dict:
            for x in validated_dict[u'variables']:
                if 'description' in x  or 'name' in x or 'standard_name' in x:
                    new_item ={}
                    new_item[u'name'] = u'Variables'
                    new_item[u'value'] = x['description'] if 'description' in x else x['name']
                    variables.append(new_item)

        try:
            search_data['extras_variables'] = self._prepare_list_for_index(validated_dict[u'variables'])  # noqa
            search_data['extras_dimensions'] = self._prepare_list_for_index(validated_dict[u'dimensions'])  # noqa
            search_data['extras_relations'] = self._prepare_list_for_index(validated_dict[u'relations'])  # noqa
            search_data['extras_specifics'] = self._prepare_list_for_index(validated_dict[u'specifics'])  # noqa

            search_data['res_hash'] = [ d['hash'] for d in validated_dict[u'resources'] if d['hash'] not in '' ]

            # Flatten specifics
            # i.e: Add the new search items extras_specifcs_*
            search_data.update(self._flatten_list_for_index(validated_dict[u'specifics'], 'extras_specifics', 'name', 'value'))

            # Add the new search item extras_specifcs_Variables
            search_data.update(self._flatten_list_for_index(variables, 'extras_specifics', 'name', 'value'))

        except:
            print "before-index: something did not work"
            pass

        return search_data

    # generates a set with all dicts from list
    def _prepare_list_for_index(self, list_dicts):
        dicts = []
        for d in list_dicts:
            dicts.append(dump_json(d))

        return dicts

    def _flatten_list_for_index(self, list_dicts, result_key_prefix, filter_key, filter_value):
        unique_keywords = set([dic.get(filter_key) for dic in list_dicts])
        flatten_dict = {}
        for keyword in unique_keywords:
            flatten_dict.update(
                {'_'.join([result_key_prefix, keyword]): [d.get(filter_value) for d in list_dicts if d.get(filter_key) in keyword ]})

        return flatten_dict
