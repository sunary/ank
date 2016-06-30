__author__ = 'sunary'


from apps._app import App
from queue.rabbit_mqueue import Queue


class RabbitMqProducer(App):
    '''
    Push message(s) to queue
    '''
    def __init__(self, uri, name):
        '''
        Args:
            uri: list of uri connections.
            name: queue name, end by 'Exchange' is exchange.
        Examples:
            >>> Queue(uri=['amqp://username:password@host:5672/'], name='ExampleExchange')
        '''
        super(RabbitMqProducer, self).__init__()

        self.queue = Queue(uri, name)

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        if messages:
            self.queue.post(messages)

        return messages