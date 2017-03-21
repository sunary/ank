__author__ = 'sunary'


from apps.app import BaseApp
import pika


class RabbitmqProducer(BaseApp):
    '''
    Push message to queue
    '''
    def __init__(self, uri, exchange, routing_key):
        '''
        Args:
            uri: uri connections.
            exchange: exchange name.
            routing_key: routing key.
        Examples:
            >>> RabbitmqProducer(uri='amqp://username:password@host:5672',
            ... exchange='ExampleExchange',
            ... routing_key='ExchangeToQueue')
        '''
        super(RabbitmqProducer, self).__init__()

        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.channel = self.connection.channel()

    def run(self, process=None):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing_key,
                                   body=message)
        return message

    def close_connection(self):
        self.connection.close()