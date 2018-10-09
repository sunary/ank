__author__ = 'sunary'


from ank.core.app import App


class KafkaProducer(App):
    """
    Push message to queue
    """

    def __init__(self):
        self.producer = None
        self.topic = None

    def init_app(self, producer=None, topic=''):
        """
        Args:
            producer (kafka.KafkaProducer): kafka producer
            topic (string): kafka subscriber topic
        """
        self.producer = producer
        self.topic = topic

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.producer.send(self.topic, message)
        return message
