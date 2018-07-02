__author__ = 'sunary'


from ank.apps.pipe_app import PipeApp


class RedisSubscribe(PipeApp):
    """
    Subscribe message from redis pubsub
    """

    def ini_app(self, redis=None, topic=''):
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
