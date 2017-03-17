import os
import shutil

import ckan.lib.helpers as h
import ckan.lib.base as base
import requests
from pylons import config
import ckan.plugins.toolkit as toolkit

import cgi
import logging
import json
import pathlib2
import ckan.model as model
import ckan.logic as logic
import ckan.lib.uploader as uploader
import pprint
import ast
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

        result = []

        if thesaurus == "":
            taxonomy_term = get_action('taxonomy_term_show')(context, {'label': label})

            taxonomy_id = taxonomy_term['taxonomy_id']
            taxonomy = get_action('taxonomy_show')(context, {'id': taxonomy_id})
        else:
            taxonomy = get_action('taxonomy_show')(context, {'name': thesaurus})
            taxonomy_term = get_action('taxonomy_term_show')(context, {'label': label, 'taxonomy_id': taxonomy['id']})

        result = [taxonomy['name']]
        result.append(taxonomy_term['uri'])

        return json.dumps(result)
