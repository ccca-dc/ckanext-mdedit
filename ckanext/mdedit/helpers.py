import re
import datetime
import pytz

from pylons import config
from pylons.i18n import gettext

import json
import ckan.logic as logic
get_action = logic.get_action


""" Anja 29.9.2016 """
import  ckan.plugins.toolkit as tk
context = tk.c
import ckan.lib.base as base
Base_c = base.c
from pylons import c
import logging
log = logging.getLogger(__name__)
""" Anja 29.9.2016 """
""" Anja 23.11.2016 """
import random
""" Anja 23.11.2016 """
""" Georg 2017-02-09 """
import ckan.lib.formatters as formatters

global_contains_field = []

def mdedit_get_name():
     # Get the user name of the logged-in user.
    # log.debug("Helpers mdedit_get_name")

    user = c.userobj
    # log.debug(c)
    # log.debug(user)

    if user:
        u = gettext(user)
        if isinstance(u, str):
            return u.decode('utf-8')
        return  user.fullname
    else:
        return None

def mdedit_get_name_citation():
     # Get the user name of the logged-in user.

    user = c.userobj
    if user:
        cite_name = user.fullname
        if cite_name != "" and cite_name != None:
            cite_name = cite_name.split()
            cite_name = cite_name[len(cite_name)-1]
            cite_name += " et al"
            return cite_name
    else:
        return "Smith et al"

def mdedit_get_mail():
     # Get the user mailaddress of the logged-in user.
    user = c.userobj
    if user:
        return user.email
    else:
        return None

def mdedit_get_date():
    now = datetime.datetime.today()
    # now =now.strftime('%d %B %Y')
    return now

def mdedit_parse_date(mdedit_date):
    # log.debug("Helpers mdedit_parse_date; date: " + mdedit_date)
    # log.debug("Helpers mdedit_parse_date; type:")
    # log.debug(type(mdedit_date))
    return mdedit_date

def mdedit_get_contain_labels(field):

    #log.debug("mdedit_get_contain_labels *********** Anja ******************")

    num = int(field['contains'])
    #print num

    labels = []

    for i in range (1,num+1):
        #print i
        id = 'l'+ str(i)
        labels.append (field[id])

    #print labels
    return labels

def mdedit_get_contain_pholders(field):

    #log.debug("mdedit_get_contain_pholders *********** Anja ******************")

    num = int(field['contains'])
    #print num

    pholders = []

    for i in range (1,num+1):
        #print i
        id = 'p'+ str(i)
        pholders.append (field[id])

    #print pholders
    return pholders

def mdedit_get_contain_values(data, field):
    # Turn String into list again
    # and extract the required fields (index)

    #print "mdedit_get_contain_values *********** Anja ******************"
    #print field['field_name']
    #print field

    otto = c.pkg_dict

#    print "********** Anja: DATA"
#    print data.get(field['field_name'])

    if data:
        cu = data.get(field['field_name'])
        #print "******** Anja 1 data"
    else:
        if otto:
            cu = c.pkg_dict.get(field['field_name'])
            #print "******** Anja 2 pkg_dict"

    if not cu:
      return ""

    if not isinstance(cu, list):
        try:
            clist = json.loads(cu)
        except:
            return ""
    else:
        clist = cu

    #print clist
    #print (type(clist))

    num_contains = int (field['contains'])

    # Sort values according to num items in field
    values =[[] for x in range(num_contains)]
    for j in range(num_contains):
        for i in range(j,len(clist),num_contains):
            values[j].append(clist[i])

    return values

def mdedit_render_size(value):
    # Render Size String from Resource
    if value is not None:
        value = formatters.localised_filesize(int(value))
    return value


def mdedit_get_taxonomies():
    context = {'user': c.user}
    taxonomy_list = get_action('taxonomy_list')(context, {})
    return taxonomy_list


def mdedit_parse_used_thesauri(mdedit_used_thesauri):
    mdedit_used_thesauri = json.loads(mdedit_used_thesauri)

    thesauri = []

    for t in mdedit_used_thesauri:
        thesaurus = t['taxonomy']
        if thesaurus != "" and thesaurus not in thesauri:
            thesauri.append(thesaurus.strip())

    return ', '.join(thesauri)
