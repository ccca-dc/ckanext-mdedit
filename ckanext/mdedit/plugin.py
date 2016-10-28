import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.mdedit import helpers

class MdeditPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    #plugins.implements(plugins.IDatasetForm, inherit=True)

    #FALLBACK_OPTION = 'scheming.dataset_fallback'


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
            'mdedit_get_date': helpers.mdedit_get_date
            }

     # Package Form
    #@classmethod
    #def package_form(self):
    #    return 'mdedit/package/snippets/package_form.html'
