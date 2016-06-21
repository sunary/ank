__author__ = 'sunary'


from redis import StrictRedis


redis = StrictRedis()
expire = 60 * 84600


def get(key, func=None, extraArgs=None):
    exist_value = redis.get(key)

    if not exist_value and func:
        new_value = func(*extraArgs)
        set(key, new_value)
        return new_value
    else:
        return exist_value


def set(key, value):
    redis.set(key, value)
    redis.expire(key, expire)