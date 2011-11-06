from flask import Flask
from flask import render_template
from flask import request


## Don't forget to enter your own API keys into the secrets file! 
from rovi import get_artist, get_artist_by_name, get_autocomplete, get_verbose_album, get_filterbrowse_christmas, get_filterbrowse_christmas_full, get_best_image

import urllib
import json
import time
import re

app = Flask (__name__)

# Don't show christmas or holidays
bad_styles = ['MA0000011929', 'MA0000012148']
banned_styles = set(bad_styles)


f = open("topitemmap.json", "r")
topitems = json.load(f)
f.close()

f = open("styles.json", "r")
style_map = json.load(f)
f.close()

f = open("images.json", "r")
image_map = json.load(f)
f.close()

reverse_style_map = {}
alpha_styles = []

for key, val in style_map.iteritems():
    if key in topitems:
        reverse_style_map[val] = key
        alpha_styles.append(val)

alpha_styles.sort()

@app.route('/')
def index():
    params = []
    params.append(('facet', "genre"))
    response = get_filterbrowse_christmas_full(params)
    facets = response["searchResponse"]["facetCounts"][0]["facetCount"]
    
    facet_hash = {}
    for facet in facets:
        facet_hash[facet["name"]] = facet["id"]
    
    return render_template('index.html', facet_hash=facet_hash, alpha_styles=alpha_styles, reverse_style_map=reverse_style_map)

@app.route('/show/albumfromgenre/<genreid>')
def album_from_genre(genreid):
    params = []
    params.append(('filter', "genreid:" + genreid))
    params.append(('size', 1))
    results = get_filterbrowse_christmas(params)
    albumid = results[0]["id"]
    return show_album(albumid)

@app.route('/show/albumfromstyle/<genreid>')
def album_from_style(genreid):
    params = []
    params.append(('filter', "subgenreid:" + genreid))
    params.append(('size', 1))
    results = get_filterbrowse_christmas(params)
    albumid = results[0]["id"]
    return show_album(albumid)

@app.route('/show/artist/<artist>')
def show_artist(artist):

    artist = get_artist_by_name(artist)

    artist_info = {}
    artist_info["name"] = artist["name"]
    artist_info["birth"] = artist["birth"]["date"]
    artist_info["home"] = artist["birth"]["place"]

    return render_template('artist.html', artist_info=artist_info)


@app.route('/show/album/<albumid>')
def show_album(albumid):

    album = get_verbose_album(albumid)
    
    # yank rovilinks from the description
    if album["primaryReview"] is None:
        album["primaryReview"]["text"] = "Sorry, no review available for this album".
    else:
        # just in case no bio, and it is "None"
        strip_rlinks = re.compile('(\[.+?\])', re.DOTALL)
        album["primaryReview"]["text"] = strip_rlinks.sub('', album["primaryReview"]["text"])

    styles = album["styles"] 
    #moods = album["moods"] 
    #themes = album["themes"] 
    
    image_url = get_best_image(album)

    style_hash = {}
    #mood_hash = {}
    #theme_hash = {}
    image_hash = {}

    #for theme in themes:
    #   params = []
    #    params.append(('filter', "themeid:" + theme["id"]))
    #    params.append(('include', "images"))
    #    results = get_filterbrowse_christmas(params)
    #    theme_hash[theme["id"]] = results

    #for mood in moods:
    #    params = []
    #    params.append(('filter', "moodid:" + mood["id"]))
    #    params.append(('include', "images"))
    #   results = get_filterbrowse_christmas(params)
    #    mood_hash[mood["id"]] = results

    for style in styles:
        if style["id"] in banned_styles:
            continue
        params = []
        params.append(('filter', "subgenreid:" + style["id"]))
        params.append(('include', "images"))
        results = get_filterbrowse_christmas(params)
        style_hash[style["id"]] = results

    return render_template('album.html', album=album, hello="hello world", image_map=image_map,
                           image_url=image_url, style_hash=style_hash)


@app.route('/autocomplete/<query>')
def autocomplete(query):

    autocomplete = get_autocomplete(query)

    autocomplete_info = autocomplete["autocompleteResponse"]["results"]

    return render_template('autocomplete.html', autocomplete=autocomplete_info)


@app.route('/filterbrowse/mood/<descid>')
def filterbrowse_mood(descid):

    params = []
    params.append(('filter', "moodid:" + descid))
    results = get_filterbrowse_christmas(params) 
    
    return render_template('filterbrowse.html', results=results)

@app.route('/filterbrowse/style/<descid>')
def filterbrowse_style(descid):

    params = []
    params.append(('filter', "subgenreid:" + descid))
    results = get_filterbrowse_christmas(params) 
    
    return render_template('filterbrowse.html', results=results)


@app.route('/filterbrowse/theme/<descid>')
def filterbrowse_theme(descid):

    params = []
    params.append(('filter', "themeid:" + descid))
    results = get_filterbrowse_christmas(params) 
    
    return render_template('filterbrowse.html', results=results)


@app.route('/show/name/<name>')
def show_name(name):
    return render_template('name.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.logger.debug('The logger is running, hooray!')
    
    
    


#def hash_images(results):
#    imghash = {}
#    for result in results:

#        images = result["album"]["
