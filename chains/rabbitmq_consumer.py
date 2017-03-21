__author__ = 'sunary'


from apps.app import BaseApp
import pika


class RabbitmqConsumer(BaseApp):
    '''
    Message was received from queue by on_messages_received() method
    '''

    def __init__(self, uri, queue):
        '''
        Args:
            uri: uri connections.
            queue: queue name.
        Examples:
            >>> RabbitmqConsumer(uri='amqp://username:password@host:5672',
            ... queue='ExampleQueue')
        '''
        BaseApp.__init__(self)
        connection = pika.BlockingConnection(pika.URLParameters(uri))
        channel = connection.channel()
        channel.basic_consume(self.process, queue=queue, no_ack=True)

        channel.start_consuming()

    def run(self, process=None):
        BaseApp.run(self, process)

    def process(self, ch, method, properties, message):
        return message