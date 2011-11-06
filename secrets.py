import time
import hashlib


# Rovi Secrets
APIKEY = '3jedgsyd8f7m6c2r4bqvfkqa'
SECRET = 'pz5E41N6bR'

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
