import re
import datetime
import pytz

from pylons import config
from pylons.i18n import gettext

from ckanapi import LocalCKAN, NotFound, NotAuthorized
""" Anja 29.9.2016 """
import  ckan.plugins.toolkit as tk
context = tk.c
import ckan.lib.base as base
c = base.c
from pylons import c
import logging
log = logging.getLogger(__name__)
""" Anja 29.9.2016 """

def mdedit_get_name():
     # Get the user name of the logged-in user.
    user = c.userobj
    return user.fullname

def mdedit_get_mail():
     # Get the user mailaddress of the logged-in user.
    user = c.userobj
    return user.email

def mdedit_get_date():
    now = datetime.datetime.today()
    # now =now.strftime('%d %B %Y')
    return now
