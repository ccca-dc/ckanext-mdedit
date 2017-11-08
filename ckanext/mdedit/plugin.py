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
    parse_json, map_to_valid_format
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
            }

    # IActions
    def get_actions(self):
        actions = {'package_contact_show': action.package_contact_show}
        return actions

    # ITemplateHelpers
    def get_helpers(self):
        return {
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
            'get_readable_file_size': helpers.get_readable_file_size,
            'get_frequency_name': helpers.get_frequency_name
            }


class MdeditLanguagePlugin(plugins.SingletonPlugin):
    """
    Handles language dictionaries in data_dict (pkg_dict).
    """

    def before_view(self, pkg_dict):
        pkg_dict = self._prepare_package_json(pkg_dict)

        return pkg_dict

    def _ignore_field(self, key):
        return False

    def _prepare_package_json(self, pkg_dict):
        # parse all json strings in dict
        pkg_dict = self._package_parse_json_strings(pkg_dict)

        # map ckan fields
        pkg_dict = self._package_map_ckan_default_fields(pkg_dict)

        # prepare format of resources
        # pkg_dict = self._prepare_resources_format(pkg_dict)

        try:
            # Do not change the resulting dict for API requests
            path = pylons.request.path
            if path.startswith('/api'):
                return pkg_dict
        except TypeError:
            # we get here if there is no request (i.e. on the command line)
            return pkg_dict

        # replace langauge dicts with requested language strings
        # desired_lang_code = self._get_request_language()
        # pkg_dict = self._package_reduce_to_requested_language(
        #     pkg_dict, desired_lang_code
        # )

        return pkg_dict

    def _get_request_language(self):
        try:
            return pylons.request.environ['CKAN_LANG']
        except TypeError:
            return pylons.config.get('ckan.locale_default', 'en')

    def _package_parse_json_strings(self, pkg_dict):
        # try to parse all values as JSON
        for key, value in pkg_dict.iteritems():
            pkg_dict[key] = parse_json(value)

        return pkg_dict


    def _package_map_ckan_default_fields(self, pkg_dict):  # noqa
        # Map Maintainer and author from contact_points
        if pkg_dict.get('maintainer') is None:
            try:
                pkg_dict['maintainer'] = pkg_dict['contact_points'][0]['name']  # noqa
            except (KeyError, IndexError):
                pass

        if pkg_dict.get('maintainer_email') is None:
            try:
                pkg_dict['maintainer_email'] = pkg_dict['contact_points'][0]['email']  # noqa
            except (KeyError, IndexError):
                pass

        if pkg_dict.get('author') is None:
            try:
                pkg_dict['author'] = pkg_dict['contact_points'][0]['name']  # noqa
            except (KeyError, IndexError):
                pass

        if pkg_dict.get('author_email') is None:
            try:
                pkg_dict['author_email'] = pkg_dict['contact_points'][0]['email']  # noqa
            except (KeyError, IndexError):
                pass

        # Map Temporals for DCAT Export
        # TODO Support multiple temporal extents
        if pkg_dict.get('temporal_start') is None:
            try:
                pkg_dict['temporal_start'] = pkg_dict['temporals'][0]['start_date']  # noqa
            except (KeyError, IndexError):
                pass

        if pkg_dict.get('temporal_end') is None:
            try:
                pkg_dict['temporal_end'] = pkg_dict['temporals'][0]['end_date']  # noqa
            except (KeyError, IndexError):
                pass

        return pkg_dict

    def _prepare_resources_format(self, pkg_dict):
        if pkg_dict.get('resources') is not None:
            for resource in pkg_dict['resources']:
                resource = self._prepare_resource_format(resource)

                # if format could not be mapped and media_type exists use this value  # noqa
                if (not resource.get('format') and resource.get('media_type')):
                    resource['format'] = resource['media_type'].split('/')[-1]

        return pkg_dict

    # Generates format of resource and saves it in format field
    def _prepare_resource_format(self, resource):
        resource_format = ''

        # get format from media_type field if available
        if not resource_format and resource.get('media_type'):  # noqa
            resource_format = resource['media_type'].split('/')[-1].lower()

        # get format from format field if available (lol)
        if not resource_format and resource.get('format'):
            resource_format = resource['format'].split('/')[-1].lower()

        # check if 'media_type' or 'format' can be mapped
        has_format = (map_to_valid_format(resource_format) is not None)

        # if the fields can't be mapped,
        # try to parse the download_url as a last resort
        if not has_format and resource.get('download_url'):
            path = urlparse.urlparse(resource['download_url']).path
            ext = os.path.splitext(path)[1]
            if ext:
                resource_format = ext.replace('.', '').lower()

        mapped_format = map_to_valid_format(resource_format)
        if mapped_format:
            # if format could be successfully mapped write it to format field
            resource['format'] = mapped_format
        elif not resource.get('download_url'):
            resource['format'] = 'SERVICE'
        else:
            # else return empty string (this will be indexed as N/A)
            resource['format'] = ''

        return resource



class MdeditResourcePlugin(MdeditLanguagePlugin):
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
        return key == 'tracking_summary'


class MdeditPackagePlugin(MdeditLanguagePlugin):
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

        return pkg_dict

#    def before_index(self, search_data):
#        if not self.is_supported_package_type(search_data):
#            return search_data
#
#        validated_dict = json.loads(search_data['validated_data_dict'])
#
#        search_data['res_format'] = self._prepare_formats_for_index(validated_dict[u'resources'])  # noqa
#        search_data['title_string'] = extract_title(validated_dict)
#        search_data['description'] = LangToString('description')(validated_dict)  # noqa
#        if 'political_level' in validated_dict[u'organization']:
#            search_data['political_level'] = validated_dict[u'organization'][u'political_level']  # noqa
#
#        try:
#            # index language-specific values (or it's fallback)
#            text_field_items = {}
#            for lang_code in get_langs():
#                search_data['title_' + lang_code] = get_localized_value(
#                    validated_dict['title'],
#                    lang_code
#                )
#                search_data['title_string_' + lang_code] = munge_title_to_name(
#                    get_localized_value(validated_dict['title'], lang_code)
#                )
#                search_data['description_' + lang_code] = get_localized_value(
#                    validated_dict['description'],
#                    lang_code
#                )
#                search_data['keywords_' + lang_code] = get_localized_value(
#                    validated_dict['keywords'],
#                    lang_code
#                )
#
#                text_field_items['text_' + lang_code] = [get_localized_value(validated_dict['description'], lang_code)]  # noqa
#                text_field_items['text_' + lang_code].extend(search_data['keywords_' + lang_code])  # noqa
#                text_field_items['text_' + lang_code].extend([r['title'][lang_code] for r in validated_dict['resources'] if r['title'][lang_code]])  # noqa
#                text_field_items['text_' + lang_code].extend([r['description'][lang_code] for r in validated_dict['resources'] if r['description'][lang_code]])  # noqa
#
#            # flatten values for text_* fields
#            for key, value in text_field_items.iteritems():
#                search_data[key] = ' '.join(value)
#
#        except KeyError:
#            pass
#
#        return search_data
#
#    # generates a set with formats of all resources
#    def _prepare_formats_for_index(self, resources):
#        formats = set()
#        for r in resources:
#            resource = self._prepare_resource_format(r)
#            if resource['format']:
#                formats.add(resource['format'])
#            else:
#                formats.add('N/A')
#
#        return formats
