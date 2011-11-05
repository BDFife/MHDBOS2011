import urllib
import json
import hashlib
import logging
from secrets import apikey, sign

# Rovi Secrets
HOSTNAME = 'api.rovicorp.com'
NAMEPATH = 'data/v1/name'
MUSICPATH = 'search/v2/music'
F = 'search/v2/music'

def get_artist(id):
    params = []
    params.append(('id', id))

    return get_rovi_response(NAMEPATH, 'info', params)

def get_artist_by_name(name):
    params = []
    params.append(('name', name))
    return get_rovi_response(NAMEPATH, 'info', params)


def get_autocomplete(query):
    params = []
    if isinstance(query, unicode):
        query = query.encode('utf-8')
    params.append(('query', query))
    params.append(('entitytype', 'artist'))
    params.append(('size', 10))
    return get_rovi_response(MUSICPATH, 'autocomplete', params)

def get_rovi_response(path, method, param_list):
    param_list.append(('apikey', apikey()))
    param_list.append(('sig', sign()))
    param_list.append(('format', 'json'))

    params = urllib.urlencode(param_list)
    
    url = 'http://%s/%s/%s' % (str(hostname()) , str(path), str(method))
    
    url = url + '?' + params
    
    print url
    
    f = urllib.urlopen(url)
    response_dict = json.loads(f.read())
    
    return response_dict


def hostname():
    return HOSTNAME

