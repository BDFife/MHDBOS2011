import urllib, urllib2, urllib3
import json
from xml.dom import minidom
import time
import hashlib
import logging
from secrets import key, sign

# Rovi Secrets
HOSTNAME = 'api.rovicorp.com'
NAMEPATH = 'data/v1/name'
MUSICPATH = 'search/v2/music'

def get_artist(id):
    params = {}
    params['id'] = id
    return get_rovi_response(NAMEPATH, 'info', params)

def get_artist_by_name(name):
    params = {}
    params['name'] = name
    return get_rovi_response(NAMEPATH, 'info', params)


def get_autocomplete(query):
    params = {}
    params['query'] = query
    params['entitytype'] = 'artist'
    params['size'] = 10
    return get_rovi_response(MUSICPATH, 'autocomplete', params)

def get_rovi_response(path, method, param_dict):
    param_dict['apikey'] = apikey()
    param_dict['sig'] = sign()
    param_dict['format'] = 'json'
    param_list = []

    for key,val in param_dict.iteritems():
        if isinstance(val, list):
            param_list.extend( [(key,subval) for subval in val] )
        elif val is not None:
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            param_list.append( (key,val) )

    params = urllib.urlencode(param_list)
    
    url = 'http://%s/%s/%s' % (str(hostname()) , str(path), str(method))
    
    url = url + '?' + params
    
    print url
    
    f = urllib.urlopen(url)
    response_dict = json.loads(f.read())
    
    return response_dict


def hostname():
    return HOSTNAME

