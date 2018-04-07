import memcache

MEMCACHE_HOST = '127.0.0.1'
MEMCACHE_PORT = 11211

CACHE = memcache.Client([(MEMCACHE_HOST, MEMCACHE_PORT)])


def cache(time=0):
    """
    Use the first argument as the key and try to get it from the cache. If it
    doesn't exist run the function and put the return value in the cache.
    """
    def wrap(function):
        def wrapped(*args):
            key = str(args[0])
            key = key.replace(' ', '_')
            if CACHE.get(key):
                return CACHE.get(key)

            result = function(*args)
            CACHE.set(key, result, time=time)
            return result
        return wrapped
    return wrap
