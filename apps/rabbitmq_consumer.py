__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
try:
    import pika
except ImportError:
    raise ImportError('pika not found')


class RabbitmqConsumer(PipeApp):
    """
    Message was received from queue by on_messages_received() method
    """

    def init_app(self, uri='', queue=''):
        """
        Args:
            uri (string): connection uri
            queue (string): queue name
        Examples:
            >>> RabbitmqConsumer(uri='amqp://username:password@host:5672',
            ... queue='ExampleQueue')
        """
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.queue = queue

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))
        channel = self.connection.channel()
        channel.basic_consume(self.call_back, queue=self.queue, no_ack=True)

        channel.start_consuming()

    def call_back(self, ch, method, properties, message):
        return self.process(message)

    def process(self, message):
        return message
