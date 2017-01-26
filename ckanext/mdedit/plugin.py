import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.mdedit import helpers
from ckanext.mdedit import validators
ignore_empty = plugins.toolkit.get_validator('ignore_empty')


class MdeditPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    #plugins.implements(plugins.IRoutes, inherit=True)
    #plugins.implements(plugins.IDatasetForm, inherit=True)


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mdedit')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'mdedit_get_name': helpers.mdedit_get_name,
            'mdedit_get_mail': helpers.mdedit_get_mail,
            'mdedit_get_date': helpers.mdedit_get_date,
            'mdedit_parse_date': helpers.mdedit_parse_date,
            'mdedit_get_name_citation': helpers.mdedit_get_name_citation,
            'mdedit_get_contain_values': helpers.mdedit_get_contain_values,
            'mdedit_get_contain_labels': helpers.mdedit_get_contain_labels,
            'mdedit_get_contain_pholders': helpers.mdedit_get_contain_pholders
            }

    # IValidators
    def get_validators(self):
        return {
            'mdedit_contains': validators.mdedit_contains
            }
