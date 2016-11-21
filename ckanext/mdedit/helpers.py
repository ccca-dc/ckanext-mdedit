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

""" Anja 21.11.2016 """
import ckan.lib.search as search
from ckan import model
""" Anja 21.11.2016 """


def mdedit_get_name():
     # Get the user name of the logged-in user.
    log.debug("Helpers mdedit_get_name")

    user = c.userobj
    log.debug(c)
    log.debug(user)
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
    log.debug("Helpers mdedit_parse_date; date: " + mdedit_date)
    log.debug("Helpers mdedit_parse_date; type:")
    log.debug(type(mdedit_date))
    return mdedit_date

def mdedit_count_resources():
    log.debug("mdedit_count_resources ******************")

    """ Anja 21.11.2016
    Attention: Hard limit of 1000 Datasets - parameter obviously "rows" not "limit" ...
    """

    all_sets = logic.get_action('package_search')({}, {"rows": 1000})
    all_count = all_sets['count']
    log.debug(all_sets['count'])

    if all_count > 999:
        all_count = 999

    current_set = 0
    all_resource_count = 0
    while current_set < c.package_count:
        log.debug(" Loop ******************")
        log.debug(current_set)
        log.debug(all_sets['results'][current_set]['id'])
        all_sets['results'][current_set]['title']
        log.debug(all_sets['results'][current_set]['num_resources'])
        all_resource_count += all_sets['results'][current_set]['num_resources']
        current_set += 1
        log.debug(all_resource_count)

    log.debug("mdedit_count_resources ******************")
    return all_resource_count

""" Anja 21.11.2016



    while current_set < c.package_count:
        all_resource_count += otto['results'][current_set]['num_resources']
        i += 1
    otto = logic.get_action('package_search')({}, {})


    log.debug(otto['results'][4]['num_resources'])


    stats['dataset_count'] = logic.get_action('package_search')(
    {}, {"rows": 1})['count']
    log.debug(c.datasets)
    log.debug("otto")
    log.debug(c.package_count)
    all_sets = c.datasets
    log.debug("otto")
    num_sets = c.package_count
    all_resource_count = 0
    log.debug(num_sets)
    if hasattr(c, "foo"):
        x = c.foo
    else:
        x = 'default'
    i = 0
    while i < c.package_count:
        log.debug("emil")
        all_resource_count += c.datasets[i].num_resources
        i += 1
    log.debug("mdedit_count_resources ******************")

    return all_resource_count
"""
