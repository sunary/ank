__author__ = 'sunary'


from apps._app import App
from queue.queue import QueueConnection
from kombu.mixins import ConsumerMixin
import kombu


class GetMessage(App, ConsumerMixin):

    '''
    Consumer process,
    process one message,
    messages were received from queue by on_messages_received() method
    '''

    def __init__(self, queue_config, batch_size=100):
        App.__init__(self)

        self.queue_connection = QueueConnection(';'.join(queue_config.get('uri')))
        self.queue_connection.connect()

        self.connection = self.queue_connection._connection
        self.queue = kombu.Queue(queue_config.get('name'))
        self.prefetch_count = queue_config.get('prefetch_count', batch_size)

    def run(self, process=None):
        App.run(self, process)

    def get_consumers(self, Consumer, channel):
        consumer = Consumer(queues=[self.queue], callbacks=[self.on_message_received])
        consumer.qos(prefetch_count=self.prefetch_count)
        return [consumer,]

    def on_message_received(self, payload, message):
        last_id_process = -1
        status = []
        try:
            for i in range(len(payload)):
                _status = self._process(payload[i])
                status.append(_status)

                if _status:
                    message[i].ack()
                    last_id_process = i
                else:
                    message[i].requeue()
        except Exception as e:
            self.logger.error(e)
            for i in range(last_id_process + 1, len(payload)):
                message[i].requeue()

        return status

    def process(self, messages=None):

        return messages