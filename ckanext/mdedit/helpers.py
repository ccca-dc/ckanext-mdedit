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
import ckan.lib.helpers as hck

import ckan.model as model


global_contains_field = []

###################### End Copied from Kathi ##############

def get_older_versions(resource_id, package_id):
    ctx = {'model': model}

    pkg = logic.get_action('package_show')(ctx, {'id': package_id})
    resource = logic.get_action('resource_show')(ctx, {'id': resource_id})
    resource_list = pkg['resources']

    versions = []

    # get older versions
    res_helper = resource.copy()
    while res_helper is not None:
        res_id = res_helper['id']
        res_helper = None
        for res in resource_list:
            if 'newer_version' in res and res['newer_version'] == res_id:
                versions.append({'id': res['id'], 'created': res['created'], 'current': False})
                res_helper = res.copy()
                break

    # get this version
    versions.insert(0, {'id': resource['id'], 'created': resource['created'], 'current': True})

    # get newer versions
    if 'newer_version' in resource and resource['newer_version'] != "":
        newest_resource = tk.get_action('resource_show')(data_dict={'id': resource['newer_version']})

        versions.insert(0, {'id': newest_resource['id'], 'created': newest_resource['created'], 'current': False})

        has_newer_version = True
        while has_newer_version is True:
            has_newer_version = False
            for res in resource_list:
                if 'newer_version' in newest_resource and newest_resource['newer_version'] == res['id']:
                    versions.insert(0, {'id': res['id'], 'created': res['created'], 'current': False})
                    newest_resource = res.copy()
                    has_newer_version = True
                    break

    return versions

###################### End Copied from Kathi ##############

def mdedit_get_package_id(resource_id):

    res = tk.get_action('resource_show')(data_dict={'id': resource_id})
    if 'package_id' in res:
        return res['package_id']
    else:
        return ""
    

def mdedit_get_resource_title(resource_id):

    res = tk.get_action('resource_show')(data_dict={'id': resource_id})

    result = res['name']
    if result == "":
        result = "unnamed resource"
    return result

def mdedit_get_resource_version(resource_id):
    pkg = context.package

    versions = get_older_versions(resource_id, pkg['id'])
    number = -1

    for version in versions:
         if version['current'] == True:
              number = len(versions) - versions.index(version)

    return number

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
