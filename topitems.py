
from rovi import get_stylemap, get_genremap, get_filterbrowse_christmas
import json
import time

f = open("styles.json", "r")
style_hash = json.load(f)
f.close()

top_desc_to_albums = {}

for id, name in style_hash.iteritems():
    params = []
    params.append(("filter", "subgenreid:" + id))
    params.append(("size", 15))
    filterresponse = get_filterbrowse_christmas(params)
    topitems = []
    for result in filterresponse:
        topitems.append(result["id"])
        albums[result["id"]] = result["album"]["title"]
    if topitems != []:
        top_desc_to_albums[id] = topitems
   
f = open("topitemmap.json", "w")
json.dump(top_desc_to_albums, f, indent=4)
f.close()

f = open("albumdump.json", "w")
json.dump(albums, f, indent=4)
f.close()
    