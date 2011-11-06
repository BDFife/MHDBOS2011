import urllib, urllib2
import json
import hashlib
import logging
import time
from secrets import apikey, sign

# Rovi Secrets
HOSTNAME = 'api.rovicorp.com'
NAMEPATH = 'data/v1/name'
ALBUMPATH = 'data/v1/album'
MUSICPATH = 'search/v2/music'
DESCRIPTORPATH = 'data/v1/descriptor'

debug = False

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

def get_album_image(id):
    params = []
    params.append(('albumid', id))
    response = get_rovi_response(ALBUMPATH, 'images', params)
    try:
        images = response["images"]["front"]
        return get_best_image_from_list(images)
    except:
        return None 

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
    results = {}
    try:
        results = response["searchResponse"]["results"]
    except:
        print response
    return results

def get_filterbrowse_christmas_pages():
    params = []
    params.append(('filter', 'subgenreid:MA0000011929'))
    params.append(('entitytype', 'album'))
    response = get_rovi_response(MUSICPATH, 'filterbrowse', params)
    results = {}
    try:
        results = response["searchResponse"]["totalResultCounts"]
    except:
        print response
        
    return results

# unused -- safe to remove
def get_filterbrowse_christmas_full(params):
    params.append(('filter', 'subgenreid:MA0000011929'))
    params.append(('entitytype', 'album'))
    response = get_rovi_response(MUSICPATH, 'filterbrowse', params)
    return response

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
    
    if debug:
        print url
    
    response_dict = {}
    
    if url in cache:
        response_dict = cache[url]
    else:
        
        retry = True        
        while (retry):
            f = urllib2.urlopen(url)
            http_data = f.read()
            if http_data == "":
                print "Failed on URL, retrying: " + url
                time.sleep(60)
                continue
            response_dict = json.loads(http_data)
            retry = False
             
            
    return response_dict


def hostname():
    return HOSTNAME

def get_best_image(album):
    images = album["images"]["front"]
    image_url = ""
    for image in images:
#        if image_url == "":
#            image_url = image["url"]
        if image["formatid"] == 63:
            image_url = image["url"]
            return image_url
    return image_url

def get_best_image_from_list(images):
    image_url = ""
    for image in images:
        if image["formatid"] == 63:
            image_url = image["url"]
            return image_url
    return image_url


def get_genremap():
    params = []
    params.append(('include', 'subgenres'))
    response = get_rovi_response(DESCRIPTORPATH, 'musicgenres', params)
    return response


def get_stylemap():
    params = []
    response = get_rovi_response(DESCRIPTORPATH, 'styles', params)
    return response["styles"]