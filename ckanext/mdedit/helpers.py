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

def mdedit_get_name_citation():
     # Get the user name of the logged-in user.
    # log.debug("Helpers mdedit_get_name")

    user = c.userobj
    # log.debug(c)
    # log.debug(user)


    if user:
        cite_name = user.fullname
        if cite_name != "":
            cite_name = cite_name.split()
        #    log.debug("citation: **************************")
        #    log.debug(cite_name)
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

def mdedit_my_log():

    #log.debug("mdedit_my_log ******************")

    return None
