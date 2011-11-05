from flask import Flask
from flask import render_template
from flask import request


## Don't forget to enter your own API keys into the secrets file! 
from rovi import get_artist, get_artist_by_name, get_autocomplete, get_verbose_album, get_filterbrowse_christmas

import urllib
import json
import time


app = Flask (__name__)

@app.route('/')
def index():
    return render_template('index.html', testName="Jim Rocks!")

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

    images = album["images"]["front"]
    styles = album["styles"] 
    moods = album["moods"] 
    themes = album["themes"] 
    
    image_url = ""

    for image in images:
        if image_url == "":
            image_url = image["url"]
        if image["formatid"] == 63:
            image_url = image["url"]

    style_hash = {}
    mood_hash = {}
    theme_hash = {}


    for theme in themes:
        params = []
        params.append(('filter', "themeid:" + theme["id"]))
        params.append(('include', "images"))
        results = get_filterbrowse_christmas(params) 
        theme_hash[theme["id"]] = results

    for mood in moods:
        params = []
        params.append(('filter', "moodid:" + mood["id"]))
        params.append(('include', "images"))
        results = get_filterbrowse_christmas(params) 
        mood_hash[mood["id"]] = results

    for style in styles:
        params = []
        params.append(('filter', "subgenreid:" + style["id"]))
        params.append(('include', "images"))
        results = get_filterbrowse_christmas(params) 
        style_hash[style["id"]] = results

    return render_template('album.html', album=album, hello="hello world", image_url=image_url, style_hash=style_hash, theme_hash=theme_hash, mood_hash=mood_hash)


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
