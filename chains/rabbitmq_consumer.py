__author__ = 'sunary'


from apps._app import App
from queue.rabbit_mqueue import ConsumerQueue


class RabbitMqConsumer(App, ConsumerQueue):
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

        App.__init__(self)
        ConsumerQueue.__init__(self, uri, name, batch_size)

        self.prefetch_count = batch_size

    def run(self, process=None):
        App.run(self, process)

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
            status = 'Error'
            self.logger.error(e)

            for msg in messages:
                msg.requeue()

        return status

    def process(self, messages=None):

        return messages