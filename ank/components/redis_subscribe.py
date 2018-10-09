__author__ = 'sunary'


from ank.core.app import App


class RedisSubscribe(App):
    """
    Subscribe message from redis pub/sub
    """

    def __init__(self):
        self.redis = None
        self.topic = None

    def ini_app(self, redis, topic):
        """
        Args:
            redis (redis.StrictRedis): redis client
            topic (string): redis subscriber topic
        """
        self.redis = redis
        self.topic = topic

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))
        pubsub = self.redis.pubsub(self.topic)

        while True:
            message = pubsub.get_message()
            if message:
                self.chain_process(message.get('data'))

    def process(self, message=None):
        return message
