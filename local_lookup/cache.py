import logging
import requests

from bravado.client import SwaggerClient
import memcache

MEMCACHE_HOST = '127.0.0.1'
MEMCACHE_PORT = 11211

log = logging.getLogger('local_lookup')

log.debug('Starting cache connection to %s:%d', MEMCACHE_HOST, MEMCACHE_PORT)
CACHE = memcache.Client([(MEMCACHE_HOST, MEMCACHE_PORT)])

def cache(function):
    """
    Use the first argument as the key and try to get it from the cache. If it
    doesn't exist run the function and put the return value in the cache.
    """
    def wrapper(*args):
        key = str(args[0])
        key = key.replace(' ', '')
        if CACHE.get(key):
            return CACHE.get(key)

        result = function(*args)
        CACHE.set(key, result)
        return result
    return wrapper
