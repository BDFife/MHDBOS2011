
from rovi import get_filterbrowse_christmas, get_filterbrowse_christmas_pages, get_best_image_from_list, get_album_image
import json
import time

f = open("albums.snapshot.json", "r")
albums = json.load(f)
f.close()

image_cache = {}
print "Time Start %s" % time.ctime()

def runstuff():
    count = 0
    for id,name in albums.iteritems():
        count += 1
        image = get_album_image(id)
        #print id
        #print image
        if (image != None):
            image_cache[id] = image
        if count % 100 == 0:
            print "Dumping after another 100 %s" % time.ctime()
            f = open("images.json", "w")
            json.dump(image_cache, f, indent=4)
            f.close()
        if count % 1000 == 0:
            return
        
runstuff()