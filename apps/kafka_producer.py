__author__ = 'sunary'


from base_apps.pipe_app import PipeApp


class KafkaAnkProducer(PipeApp):
    """
    Push message to queue
    """

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
