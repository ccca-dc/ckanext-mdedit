import re
import datetime
import pytz

from pylons import config
from pylons.i18n import gettext

import ckan.logic as logic
get_action = logic.get_action


from ckanapi import LocalCKAN, NotFound, NotAuthorized
""" Anja 29.9.2016 """
import  ckan.plugins.toolkit as tk
context = tk.c
import ckan.lib.base as base
Base_c = base.c
from pylons import c
import logging
log = logging.getLogger(__name__)
""" Anja 29.9.2016 """

def mdedit_get_org_name():

    return ""

def mdedit_get_name():
     # Get the user name of the logged-in user.
    user = c.userobj

    log.debug(c)
    log.debug(user)

    return user.fullname

def mdedit_get_mail():
     # Get the user mailaddress of the logged-in user.
    user = c.userobj
    return user.email

def mdedit_get_date():
    now = datetime.datetime.today()
    # now =now.strftime('%d %B %Y')
    return now

def mdedit_parse_date(mdedit_date):
    log.debug("Helpers mdedit_parse_date; date: " + mdedit_date)
    log.debug("Helpers mdedit_parse_date; type:")
    log.debug(type(mdedit_date))
    return mdedit_date
