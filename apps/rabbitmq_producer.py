__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
import pika


class RabbitmqProducer(PipeApp):
    '''
    Push message to queue
    '''
    def init_app(self, uri=None, exchange=None, routing_key=None):
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