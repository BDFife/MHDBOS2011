from flask import Flask
from flask import render_template
from flask import request


## Don't forget to enter your own API keys into the secrets file! 
from secrets import sign, key

import urllib
import json
import time


app = Flask (__name__)

@app.route('/')
def index():
    return render_template('index.html', testName="Jim Rocks!")

@app.route('/show/artist/<artist>')
def show_artist(artist):

    my_url = 'http://api.rovicorp.com/data/v1/name/info?apikey=' + str(key()) + '&sig=' + str(sign()) + '&name=' + str(artist)
    
    print my_url

    url_data = urllib.urlopen(my_url)
    my_data = url_data.read()
    my_data = json.loads(my_data)

    artist_info = {}
    artist_info["name"] = my_data["name"]["name"]
    artist_info["birth"] = my_data["name"]["birth"]["date"]
    artist_info["home"] = my_data["name"]["birth"]["place"]

    return render_template('artist.html', artist_info=artist_info)

@app.route('/show/name/<name>')
def show_name(name):
    return render_template('name.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.logger.debug('The logger is running, hooray!')
