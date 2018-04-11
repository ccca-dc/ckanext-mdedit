import re
import datetime
import json
import requests

from pylons.i18n import gettext
from pylons import c

from ckan.lib import base

from ckan.common import _
import ckan.model as model
import  ckan.plugins.toolkit as tk
context = tk.c

import logging
log = logging.getLogger(__name__)

global_contains_field = []

###################### Start Copied from Kathi ##############

def get_older_versions(resource_id, package_id):
    ctx = {'model': model}

    pkg = tk.get_action('package_show')(ctx, {'id': package_id})
    resource = tk.get_action('resource_show')(ctx, {'id': resource_id})
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
def mdedit_get_package_name (id):
    res = tk.get_action('package_show')({'ignore_auth': True}, data_dict={'id': id})
    return res['name']

def mdedit_get_contact_choices(field):

    # print ("mdedit_get_contact_choices *********** Anja ******************")
    # print json.dumps(field, indent=3)
    # print "*************"

    if field['form_attrs']:
        if field['form_attrs']['fields']:
            for f in field['form_attrs']['fields']:
                if f['field_name'].endswith("role"):
                    #print f['choices']
                    return f['choices']

    return ""

def mdedit_get_contact_values (data, field):
    package = c.pkg_dict

    if data:
        values = data.get(field['field_name'])
    else:
        if package:
            values = package.get(field['field_name'])

    if not values:
        return ""
    return values


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


def mdedit_get_contain_values_k(data, field):
    # Turn String into dict
    package = c.pkg_dict

    if data:
        values = data.get(field['field_name'])
    else:
        if package:
            values = package.get(field['field_name'])

    if not values:
        return ""

    if type(values) == str or type(values) == unicode:
        values = json.loads(values)

        if not isinstance(values, list):
            return ""

        for contact in values:
            labels = [x.lower() for x in mdedit_get_contain_labels(field)]
            if not all(k in contact for k in labels):
                return ""

    return values


def localize_json_title(facet_item):
    # json.loads tries to convert numbers in Strings to integers. At this point
    # we only need to deal with Strings, so we let them be Strings.
    try:
        int(facet_item['display_name'])
        return facet_item['display_name']
    except (ValueError, TypeError):
        pass
    try:
        lang_dict = json.loads(facet_item['display_name'])
        return get_localized_value(
            lang_dict,
            default_value=facet_item['display_name']
        )
    except:
        return facet_item['display_name']


def get_frequency_name(identifier):
    frequencies = {
      'http://purl.org/cld/freq/completelyIrregular': _('Irregular'),  # noqa
      'http://purl.org/cld/freq/continuous': _('Continuous'),  # noqa
      'http://purl.org/cld/freq/daily': _('Daily'),  # noqa
      'http://purl.org/cld/freq/threeTimesAWeek': _('Three times a week'),  # noqa
      'http://purl.org/cld/freq/semiweekly': _('Semi weekly'),  # noqa
      'http://purl.org/cld/freq/weekly': _('Weekly'),  # noqa
      'http://purl.org/cld/freq/threeTimesAMonth': _('Three times a month'),  # noqa
      'http://purl.org/cld/freq/biweekly': _('Biweekly'),  # noqa
      'http://purl.org/cld/freq/semimonthly': _('Semimonthly'),  # noqa
      'http://purl.org/cld/freq/monthly': _('Monthly'),  # noqa
      'http://purl.org/cld/freq/bimonthly': _('Bimonthly'),  # noqa
      'http://purl.org/cld/freq/quarterly': _('Quarterly'),  # noqa
      'http://purl.org/cld/freq/threeTimesAYear': _('Three times a year'),  # noqa
      'http://purl.org/cld/freq/semiannual': _('Semi Annual'),  # noqa
      'http://purl.org/cld/freq/annual': _('Annual'),  # noqa
      'http://purl.org/cld/freq/biennial': _('Biennial'),  # noqa
      'http://purl.org/cld/freq/triennial': _('Triennial'),  # noqa
    }
    try:
        return frequencies[identifier]
    except KeyError:
        return identifier


def get_readable_file_size(num, suffix='B'):
    try:
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            num = float(num)
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Y', suffix)
    except ValueError:
        return False


def parse_json(value, default_value=None):
    try:
        return json.loads(value)
    except (ValueError, TypeError, AttributeError):
        if default_value is not None:
            return default_value
        return value

def dump_json(value, default_value=None):
    try:
        return json.dumps(value)
    except (ValueError, TypeError, AttributeError):
        if default_value is not None:
            return default_value
        return value

def get_content_headers(url):
    response = requests.head(url)
    return response


# all formats that need to be mapped have to be entered lower-case
def map_to_valid_format(resource_format):
    format_mapping = {
        'CSV': ['csv', 'text (.csv)', 'comma ...'],
        'GeoJSON': ['geojson'],
        'GeoTIFF': ['geotiff'],
        'GPKG': ['gpkg'],
        'HTML': ['html'],
        'INTERLIS': ['interlis'],
        'JSON': ['json'],
        'KMZ': ['kmz'],
        'MULTIFORMAT': ['multiformat'],
        'ODS': ['ods', 'vnd.oas...', 'vnd.oasis.opendocument.spreadsheet'],
        'PC-AXIS': ['pc-axis file'],
        'PDF': ['pdf'],
        'PNG': ['png'],
        'RDF': ['sparql-...'],
        'SHAPEFILE': ['esri shapefile', 'esri geodatabase (....', 'esri file geodatabase', 'esri arcinfo ascii ...'],  # noqa
        'TXT': ['text', 'txt', 'text (.txt)', 'plain'],
        'TIFF': ['tiff'],
        'WCS': ['wcs'],
        'WFS': ['wfs'],
        'WMS': ['wms'],
        'WMTS': ['wmts'],
        'XLS': ['xls', 'xlsx', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'],  # noqa
        'XML': ['xml'],
        'ZIP': ['zip'],
    }
    resource_format_lower = resource_format.lower()
    for key, values in format_mapping.iteritems():
        if resource_format_lower in values:
            return key
    else:
        return None


def filesizeformat(value, binary=False):
    # copied this method from jinja 2.7
    """Format the value like a 'human-readable' file size (i.e. 13 kB,
    4.1 MB, 102 Bytes, etc).  Per default decimal prefixes are used (Mega,
    Giga, etc.), if the second parameter is set to `True` the binary
    prefixes are used (Mebi, Gibi).
    """
    bytes = float(value)
    base = binary and 1024 or 1000
    prefixes = [
        (binary and 'KiB' or 'kB'),
        (binary and 'MiB' or 'MB'),
        (binary and 'GiB' or 'GB'),
        (binary and 'TiB' or 'TB'),
        (binary and 'PiB' or 'PB'),
        (binary and 'EiB' or 'EB'),
        (binary and 'ZiB' or 'ZB'),
        (binary and 'YiB' or 'YB')
    ]
    if bytes == 1:
        return '1 Byte'
    elif bytes < base:
        return '%d Bytes' % bytes
    else:
        for i, prefix in enumerate(prefixes):
            unit = base ** (i + 2)
            if bytes < unit:
                return '%.1f %s' % ((base * bytes / unit), prefix)
        return '%.1f %s' % ((base * bytes / unit), prefix)
