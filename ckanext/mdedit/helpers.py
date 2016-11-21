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

    if all_count > 999:
        all_count = 999

    current_set = 0
    all_resource_count = 0
    while current_set < c.package_count:
        all_sets['results'][current_set]['title']
        all_resource_count += all_sets['results'][current_set]['num_resources']
        current_set += 1
    return all_resource_count
