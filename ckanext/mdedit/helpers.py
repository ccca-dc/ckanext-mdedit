import re
import datetime
import pytz

from pylons import config
from pylons.i18n import gettext

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

def mdedit_get_name():
     # Get the user name of the logged-in user.
    # log.debug("Helpers mdedit_get_name")

    user = c.userobj
    # log.debug(c)
    # log.debug(user)
    if user:
        return user.fullname
    else:
        return None

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

def mdedit_count_resources():

    """ Anja 21.11.2016
    log.debug("mdedit_count_resources ******************")
    Attention: Hard limit of 1000 Datasets - parameter obviously "rows" not "limit" ...
    """

    all_sets = logic.get_action('package_search')({}, {"rows": 1000})
    all_count = all_sets['count']

    if all_count > 999:
        all_count = 999

    current_set = 0
    all_resource_count = 0
    while current_set < c.package_count:
        all_sets['results'][current_set]['title']
        all_resource_count += all_sets['results'][current_set]['num_resources']
        current_set += 1
    return all_resource_count

def mdedit_get_number_organizations():
    # log.debug("mdedit_get_number_organization ******************")
    '''
    Code adapted from ckan: get_featured_organizations(count=1):
    '''
    config_orgs = config.get('ckan.featured_orgs', '').split()
    count = len(config_orgs)
    # log.debug(count)
    '''
    orgs = h.featured_group_org(get_action='organization_show',
                              list_action='organization_list',
                              count=count,
                              items=config_orgs)
    log.debug(orgs)
    '''
    return count

def mdedit_get_random_organization():
    # log.debug("mdedit_random_organization ******************")
    '''
    Code adapted from ckan: get_featured_organizations(count=1):
    '''
    config_orgs = config.get('ckan.featured_orgs', '').split()

    if not config_orgs:
        return ""
    # log.debug(config_orgs)

    count = len(config_orgs)
    rand_org = random.choice(config_orgs)

    # log.debug(count)
    # log.debug(rand_org)

    '''
    orgs = h.featured_group_org(get_action='organization_show',
                              list_action='organization_list',
                              count=count,
                              items=config_orgs)
    log.debug(orgs)
    '''
    return rand_org

def mdedit_get_number_groups():
    # log.debug("mdedit_get_number_groups ******************")

    '''
    Code adapted from ckan: get_featured_goups(count=1):
    '''
    config_groups = config.get('ckan.featured_groups', '').split()
    count = len(config_groups)
    # log.debug(count)

    return count

def mdedit_get_random_group():
    # log.debug("mdedit_random_group ******************")
    '''
    Code adapted from ckan: get_featured_groups(count=1):

    '''
    config_groups = config.get('ckan.featured_groups', '').split()
    # log.debug(config_groups)

    if not config_groups:
        return ""
    rand_group = random.choice(config_groups)
    # log.debug(rand_group)

    return rand_group
