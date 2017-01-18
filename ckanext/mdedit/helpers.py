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
        u = gettext(user)
        if isinstance(u, str):
            return u.decode('utf-8')
        return  user.fullname
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
        if cite_name != "" and cite_name != None:
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
def mdedit_get_contains(field_name, start_index, num_elements):
    # Turn String into list again
    # and extract the required fields (index)

    log.debug("mdedit_get_contains *********** Anja ******************")
    log.debug(start_index)
    log.debug(field_name)


    if field_name == None or start_index < 0:
        return ""

    if num_elements < start_index:
        return ""

    otto = c.pkg_dict

    if otto:
        clist = c.pkg_dict.get(field_name)
    else:
        return ""

    print (type(clist))
    print clist

    if clist:
        clist = clist.split(',')
    else:
        return ""

    print (type(clist))
    print clist

    values =[]

    for i in range(start_index,len(clist),int(num_elements)):
        print i
        print clist[i]
        values.append(clist[i])

    return values
