from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

## Don't forget to enter your own API keys into the secrets file! 
from rovi import get_artist, get_artist_by_name, get_autocomplete, get_verbose_album, get_filterbrowse_christmas, get_filterbrowse_christmas_full, get_best_image, get_genremap, get_album_tracks

import urllib
import json
import time
import re

app = Flask (__name__)


# Don't show christmas or holidays
bad_styles = ['MA0000011929', 'MA0000012148']
banned_styles = set(bad_styles)



my_url = "http://bluesock.org/~brian/topitemmap.json"
topitems = urllib.urlopen(my_url)
topitems = topitems.read()
topitems = json.loads(topitems)

my_url = "http://bluesock.org/~brian/styles.json"
style_map = urllib.urlopen(my_url)
style_map = style_map.read()
style_map = json.loads(style_map)

my_url = "http://bluesock.org/~brian/images.json"
image_map = urllib.urlopen(my_url)
image_map = image_map.read()
image_map = json.loads(image_map)

reverse_style_map = {}
alpha_styles = []

for styleid, stylename in style_map.iteritems():
    if styleid in topitems:
        use = False
        for item in topitems[styleid]:
            if item in image_map:
                use = True
        if use == True:
            reverse_style_map[stylename] = styleid
            alpha_styles.append(stylename)

alpha_styles.sort()

topitemsunicode = {}

for key, val in topitems.iteritems():
    topitemsunicode[unicode(key)] = val


def get_top_genres():
    params = []
    params.append(('facet', "genre"))
    response = get_filterbrowse_christmas_full(params)
    facets = response["searchResponse"]["facetCounts"][0]["facetCount"]
    
    facet_hash = {}
    for facet in facets:
        facet_hash[facet["id"]] = facet["name"]
    return facet_hash

genres_with_overlap = get_top_genres()
genre_tree_full = get_genremap()

genre_tree_pruned = []

for genre in genre_tree_full:

    # If top level genre doesn't overlap, continue
    if genre["id"] not in genres_with_overlap:
        continue
    
    # Otherwise grab subgenres
    subgenres_pruned = []

    for subgenre in genre["subgenres"]:
       
        # If subgenregenre doesn't overlap, continue
        if subgenre["id"] not in topitems:
            continue
 
        # Otherwise, traverse styles
        styles_pruned = []
        if unicode("styles") in subgenre:
            for style in subgenre[unicode("styles")]:
                if style["id"] in topitemsunicode:
                    # Add style to list of pruned styles
                    styles_pruned.append(style)
                    
        # If any styles overlap, map it to a special place
        if len(styles_pruned) > 0:
            subgenre["styles_pruned"] = styles_pruned
        
        # Add subgenre to lists of pruned subgenres
        subgenres_pruned.append(subgenre)
    
    # If any subgenres overlap, map it to a special place
    if len(subgenres_pruned) > 0:
        genre["subgenres_pruned"] = subgenres_pruned
       

    genre_tree_pruned.append(genre)




@app.route('/')
def index():
    params = []
    params.append(('facet', "genre"))
    response = get_filterbrowse_christmas_full(params)
    facets = response["searchResponse"]["facetCounts"][0]["facetCount"]
    
    facet_hash = {}
    for facet in facets:
        facet_hash[facet["name"]] = facet["id"]
    return render_template('index.html', facet_hash=facet_hash, alpha_styles=alpha_styles, reverse_style_map=reverse_style_map, genre_tree=genre_tree_pruned)

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
    tracks = album["tracks"]
    # yank rovilinks from the description
    if album["primaryReview"] is None:
        album["primaryReview"] = {}
        album["primaryReview"]["text"] = "Sorry, no review available for this album."
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

    seen = {}
    listsomething = []
    for style in styles:
        if style["id"] in banned_styles:
            continue
        
        styleid = unicode(style["id"])
        # For some reason if you don't ask for the type you get dups, but if you do you don't.
        # That seems bizarre, unless it's causing some conversion to happen below
        type(styleid)
        if styleid in topitems:
            items = topitems[styleid]
            positiveitems = []
            # Make sure no duplicates
            for item in items:
                if unicode(item) not in seen and item != albumid and item in image_map:
                    positiveitems.append(item)
                    seen[unicode(item)] = 1                    
            if len(positiveitems) > 1:
                style_hash[style["name"]] = positiveitems

    return render_template('album.html', album=album, hello="hello world", image_map=image_map,
                           image_url=image_url, style_hash=style_hash, tracks=tracks)


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
    app.debug = False
    app.run()
#    app.logger.debug('The logger is running, hooray!')
    
    
    


