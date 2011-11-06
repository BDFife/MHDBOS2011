import urllib
import json
import hashlib
import logging
from secrets2 import apikey, sign

# Rovi Secrets
HOSTNAME = 'api.rovicorp.com'
NAMEPATH = 'data/v1/name'
MUSICPATH = 'search/v2/music'

print "Autocomplete samples"
print "http://api.rovicorp.com/search/v2/music/autocomplete?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=artist&query=total&size=10"
print "http://api.rovicorp.com/search/v2/music/autocomplete?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&query=total&size=10"
print "http://api.rovicorp.com/search/v2/music/autocomplete?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=song&query=total&size=10"


print "Search samples"
print "http://api.rovicorp.com/search/v2/music/search?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=artist&query=total&size=10"
print "http://api.rovicorp.com/search/v2/music/search?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&query=total&size=10"
print "http://api.rovicorp.com/search/v2/music/search?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=song&query=total&size=10"


print "Filterbrowse samples"

print "http://api.rovicorp.com/search/v2/music/filterbrowse?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=artist&size=10&filter=moodid:XA0000000952"
print "http://api.rovicorp.com/search/v2/music/filterbrowse?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=artist&size=10&filter=genreid:MA0000002816"
print "http://api.rovicorp.com/search/v2/music/filterbrowse?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&size=10&filter=moodid:XA0000000952&include=moods"
print "http://api.rovicorp.com/search/v2/music/filterbrowse?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&size=10&filter=genreid:MA0000002816"


print "Recommendation Samples"

print "http://api.rovicorp.com/search/v2/music/similar?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=artist&size=10&artistid=MN0000628467"
print "http://api.rovicorp.com/search/v2/music/similar?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&size=10&albumid=MW0002110484"
print "http://api.rovicorp.com/search/v2/music/similar?apikey=" + str(apikey()) + "&sig=" + str(sign()) + "&format=json&entitytype=album&size=10&albumid=MW0002110484&filter=moodid:XA0000000952&include=Moods"
