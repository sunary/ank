__author__ = 'sunary'


from ank.apps.pipe_app import PipeApp
try:
    import pika
except ImportError:
    raise ImportError('pika not found')


class RabbitmqProducer(PipeApp):
    """
    Push message to queue
    """
    def init_app(self, uri='', exchange='', routing_key=''):
        """
        Args:
            uri (string): connection uri
            exchange (string): exchange name
            routing_key (string): routing key
        Examples:
            >>> RabbitmqProducer(uri='amqp://username:password@host:5672',
            ... exchange='ExampleExchange',
            ... routing_key='ExchangeToQueue')
        """
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.channel = self.connection.channel()

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing_key,
                                   body=message)
        return message

    def close_connection(self):
        self.connection.close()
