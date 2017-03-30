import ckan.lib.helpers as h
import ckan.lib.base as base
from pylons import config
import ckan.plugins.toolkit as toolkit

import logging
import json
import ckan.model as model
import ckan.logic as logic
import ckan.lib.uploader as uploader
import ckan.lib.navl.dictization_functions as dict_fns
from ckan.common import OrderedDict, c, g, request, _

get_action = logic.get_action
parse_params = logic.parse_params
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
abort = base.abort

check_access = logic.check_access

# c = base.c
request = base.request
log = logging.getLogger(__name__)


class TaxonomyController(base.BaseController):

    def get_taxonomy_title_from_keyword(self):
        label = request.POST.get('label')
        thesaurus = request.POST.get('thesaurus')

        context = {'model': model, 'session': model.Session,
                   'user': c.user}

        context = {'user': c.user}

        if thesaurus == "":
            try:
                term = get_action('taxonomy_term_show_all')(context, {'label': label})
            except logic.NotFound:
                result = [""]
                result.append("")

                return json.dumps(result)

            taxonomy_term = term[0]

            for t in term:
                if t['uri'] is not None and "gemet" in t['uri']:
                    taxonomy_term = t

            taxonomy_id = taxonomy_term['taxonomy_id']
            taxonomy = get_action('taxonomy_show')(context, {'id': taxonomy_id})
        else:
            taxonomy = get_action('taxonomy_show')(context, {'name': thesaurus})
            try:
                taxonomy_term = get_action('taxonomy_term_show')(context, {'label': label, 'taxonomy_id': taxonomy['id']})
            except logic.NotFound:
                result = [""]
                result.append("")
                result.append("")

                return json.dumps(result)

        result = [taxonomy['name']]
        result.append(taxonomy_term['uri'])
        result.append(taxonomy['last_modified'])

        return json.dumps(result)
