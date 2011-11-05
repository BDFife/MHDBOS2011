import time
import hashlib


# Rovi Secrets
APIKEY = 'MY API KEY'
SECRET = 'MY SECRET'

def apikey():
    return APIKEY

def secret():
    return SECRET

def sign():
    my_time = int(time.time())
    sig = hashlib.md5()
    sig.update(APIKEY)
    sig.update(SECRET)
    sig.update(str(my_time))

    return sig.hexdigest()

#if __name__ == '__main__':
#    return sign()
