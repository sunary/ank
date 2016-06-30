__author__ = 'sunary'


class KVService(object):

    def __init__(self, redis, expire=60*84600):
        '''
        Args:
            redis: redis.client.StrictRedis
            expire: expire time (seconds).
        '''
        self.redis = redis
        self.expire = expire

    def get(self, key, func=None, extraArgs=None):
        exist_value = self.redis.get(key)

        if not exist_value and func:
            new_value = func(*extraArgs)
            self.set(key, new_value)
            return new_value
        else:
            return exist_value

    def set(self, key, value):
        self.redis.set(key, value)
        self.redis.expire(key, self.expire)