import ckan.logic
import json

_get_or_bust = ckan.logic.get_or_bust
_get_action = ckan.logic.get_action


def package_contact_show(context, data_dict):
    pkg_id = _get_or_bust(data_dict, 'package_id')
    package = _get_action('package_show')(context, {'id': pkg_id})
    search_param = data_dict.pop('search_param', None)
    search_value = data_dict.pop('search_value', None)

    if package.get('contact_info', '') != '':
        contacts = json.loads(package['contact_info'])
        filtered_contacts = []
        if search_param is not None and search_value is not None and search_param.lower() in contacts[0]:
            for contact in contacts:
                if contact[search_param.lower()].lower() == search_value.lower():
                    filtered_contacts.append(contact)
            return filtered_contacts
        elif search_param is None or search_value is None:
            return contacts
    return []
