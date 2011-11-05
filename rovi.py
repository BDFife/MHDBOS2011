import urllib
import json
import hashlib
import logging
from secrets import apikey, sign

# Rovi Secrets
HOSTNAME = 'api.rovicorp.com'
NAMEPATH = 'data/v1/name'
ALBUMPATH = 'data/v1/album'
MUSICPATH = 'search/v2/music'

cache = {}


def get_artist(id):
    params = []
    params.append(('id', id))
    response = get_rovi_response(NAMEPATH, 'info', params)
    return response["name"]

def get_artist_by_name(name):
    params = []
    params.append(('name', name))
    response = get_rovi_response(NAMEPATH, 'info', params)
    return response["name"]

def get_album(id):
    params = []
    params.append(('albumid', id))
    response = get_rovi_response(ALBUMPATH, 'info', params)
    return response["album"]

def get_album(id, param_list):
    params = []
    params.append(('albumid', id))
    params.extend(param_list)
    response = get_rovi_response(ALBUMPATH, 'info', params)
    return response["album"]

def get_verbose_album(id):
    params = []
    params.append(('include', 'styles,moods,themes,primaryreview,images'))
    return get_album(id, params)
 
def get_autocomplete(query):
    params = []
    if isinstance(query, unicode):
        query = query.encode('utf-8')
    params.append(('query', query))
    params.append(('entitytype', 'artist'))
    params.append(('size', 10))
    return get_rovi_response(MUSICPATH, 'autocomplete', params)

def get_filterbrowse_christmas(params):
    params.append(('filter', 'subgenreid:MA0000011929'))
    params.append(('entitytype', 'album'))
    response = get_rovi_response(MUSICPATH, 'filterbrowse', params)
    return response["searchResponse"]["results"]

def get_filterbrowse_christmas_pages():
    params = []
    params.append(('filter', 'subgenreid:MA0000011929'))
    params.append(('entitytype', 'album'))
    response = get_rovi_response(MUSICPATH, 'filterbrowse', params)
    return response["searchResponse"]["totalResultCounts"]

def get_album_styles(id):   
    params = []
    params.append(('include', "styles"))
    album = get_album(id, params)
    styles = album["styles"]
    return styles

def get_album_moods(id):
    params = []
    params.append(('include', "moods"))
    album = get_album(id, params)
    moods = album["moods"]
    return moods

def get_album_themes(id):
    params = []
    params.append(('include', "themes"))
    album = get_album(id, params)
    themes = album["themes"]
    return themes


def get_rovi_response(path, method, param_list):
    param_list.append(('apikey', apikey()))
    param_list.append(('sig', sign()))
    param_list.append(('format', 'json'))

    params = urllib.urlencode(param_list)
    
    url = 'http://%s/%s/%s' % (str(hostname()) , str(path), str(method))
    
    url = url + '?' + params
    
    print url
    
    response_dict = {}
    
    if url in cache:
        response_dict = cache[url]
    else:
        f = urllib.urlopen(url)
        response_dict = json.loads(f.read())
        cache[url] = response_dict
        
    return response_dict


def hostname():
    return HOSTNAME

