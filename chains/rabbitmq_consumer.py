__author__ = 'sunary'


from apps.app import BaseApp
from queues.rabbit_mqueue import ConsumerQueue


class RabbitMqConsumer(BaseApp, ConsumerQueue):
    '''
    Messages were received from queue by on_messages_received() method
    '''

    def __init__(self, uri, name, batch_size=100):
        '''
        Args:
            uri: list of uri connections.
            name: queue name.
            prefetch_count: prefetch count.
        Examples:
            >>> RabbitMqConsumer(uri=['amqp://username:password@host:5672/'],
            ... name='ExampleQueue',
            ... prefetch_count=100)
        '''

        BaseApp.__init__(self)
        ConsumerQueue.__init__(self, uri, name, batch_size)

        self.prefetch_count = batch_size

    def run(self, process=None):
        BaseApp.run(self, process)

    def on_message_received(self, payloads, messages):
        try:
            status = self._process(payloads)

            if status:
                for msg in messages:
                    msg.ack()
            else:
                for msg in messages:
                    msg.requeue()
        except Exception as e:
            self.logger.error('Error when {} message {}'.format('ack' if status else 'requeue', e))

            status = 'ERROR'
            for msg in messages:
                msg.requeue()

        return status

    def process(self, messages=None):

        return messages