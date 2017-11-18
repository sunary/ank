__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
import pika


class RabbitmqConsumer(PipeApp):
    '''
    Message was received from queue by on_messages_received() method
    '''

    def init_app(self, uri=None, queue=None):
        '''
        Args:
            uri: uri connections.
            queue: queue name.
        Examples:
            >>> RabbitmqConsumer(uri='amqp://username:password@host:5672',
            ... queue='ExampleQueue')
        '''
        connection = pika.BlockingConnection(pika.URLParameters(uri))
        channel = connection.channel()
        channel.basic_consume(self.call_back, queue=queue, no_ack=True)

        channel.start_consuming()

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def call_back(self, ch, method, properties, message):
        return self.process(message)

    def process(self, message):
        return message