
from rovi import get_filterbrowse_christmas, get_filterbrowse_christmas_pages
import json


def generate_cache():
    # dragons - this function is untested. 

    cache = {}

    # determine the total size of the result and calculate # pages
    # (max response size is 100)
    page_size = 50
    result_size = get_filterbrowse_christmas_pages()
    num_pages = result_size / page_size

    print " ******************************* "
    print "Starting the caching process."
    print "Page Size: " + str(page_size)
    print "Number of Results " + str(result_size)
    print "Pages Needed " + str(num_pages)
    print " ******************************* "

    # set num_pages below if you'd like an abbreviated result. 
    #num_pages = 2

    for page in range(num_pages):

        params = []
        params.append(('size', str(page_size)))
        params.append(('include', 'styles,moods'))
        params.append(('offset', str(page*100)))

        result = get_filterbrowse_christmas(params)

        for album in result:
            cache[album["id"]] = album
            
        if page > 0:
            f = open("song_dump.json", "r")
            full_cache = json.load(f)
            f.close()
        else:
            full_cache = {}

        full_cache = (full_cache.items() + cache.items())
            
        print "Writing page " + str(page)

        f = open("song_dump.json", "w")
        json.dump(cache, f, indent=4)
        f.close()

generate_cache()

