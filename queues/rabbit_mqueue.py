__author__ = 'sunary'


import amqp
import kombu
import kombu.mixins
import time
from utilities import my_helper


logger = my_helper.init_logger(__name__)


class Message(object):

    def __init__(self):
        self.body = None
        self.tag = None


class QueueConnection(object):

    def __init__(self, uri):
        '''
        Args:
            uri: list of uri connections.
        Examples:
            >>> QueueConnection(['amqp://username:password@host:5672/'])
        '''
        self.uri = ';'.join(uri)
        self.connect()

    def connect(self):
        self._connection = kombu.connection.Connection(self.uri, failover_strategy='shuffle')
        self._connection.ensure_connection()
        self._connection.connect()

    def reconnect(self):
        try:
            self.release()
        except Exception as e:
            logger.error('Release Queue Connection: %s' % e)

        self.connect()

    def channel(self):
        return self._connection.channel()

    def re_channel(self, channel):
        try:
            channel.close()
        except Exception as e:
            logger.error('Close channel Queue Connection: %s' % e)

        while True:
            try:
                time.sleep(10)
                self.reconnect()
                return self.channel()
            except Exception as e:
                logger.error('Reconnect Queue Connection: %s' % e)

    def release(self):
        self._connection.release()


class Queue(object):

    def __init__(self, uri, name):
        '''
        Args:
            uri: list of uri connections.
            name: queue name, end by 'Exchange' is exchange.
        Examples:
            >>> Queue(uri=['amqp://username:password@host:5672/'], name='ExampleQueue')
        '''
        self.queue_name = name
        self.is_exchange = self.queue_name.endswith('Exchange')
        self.queue_connection = QueueConnection(uri)
        self.channel = self.queue_connection.channel()
        self.simple_queue = None

    def receiver(self):
        try:
            response = self.channel.basic_get(self.queue_name, no_ack=False)
        except Exception as e:
            logger.error('Queue get Response: %s' % e)

            self.channel = self.queue_connection.re_channel(self.channel)
            return None

        message = Message()
        message.body = response.body
        message.tag = response

        return message

    def delete(self, message):
        while True:
            try:
                self.channel.basic_ack(message.tag.delivery_tag)
            except Exception as e:
                logger.error('Queue ack: %s' % e)

                self.channel = self.queue_connection.re_channel(self.channel)

    def reject(self, message):
        while True:
            try:
                self.channel.basic_reject(message.tag.delivery_tag, True)
            except Exception as e:
                logger.error('Queue reject: %s' % e)

                self.channel = self.queue_connection.re_channel(self.channel)

    def post(self, payload):
        if self.is_exchange:
            message = amqp.Message(payload)
            while True:
                try:
                    self.channel.basic_publish(msg=message, exchange=self.queue_name)
                    break
                except Exception as e:
                    logger.error('Queue post to Exchange: %s' % e)

                    self.channel = self.queue_connection.re_channel(self.channel)
        else:
             while True:
                try:
                    if not self.simple_queue:
                        self.simple_queue = self.queue_connection._connection.SimpleQueue(self.queue_name)

                    self.simple_queue.put(payload)
                    break
                except Exception as e:
                    logger.error('Queue put: %s' % e)

                    self.queue_connection.reconnect()
                    if self.simple_queue:
                        self.simple_queue.close()

    def size(self):
        if self.is_exchange:
            return 0

        while True:
            try:
                queue_info = self.channel.queue_declare(queue=self.queue_name, passive=True)
                return queue_info.message_count
            except Exception as e:
                logger.error('Queue get size: %s' % e)
                self.channel = self.queue_connection.re_channel(self.channel)

    def close(self):
        try:
            if self.simple_queue is not None:
                self.simple_queue.close()
        except Exception as e:
            logger.error('Close Queue: %s' % e)

        try:
            self.channel.close()
        except Exception as e:
            logger.error('Close Channel: %s' % e)

        try:
            self.queue_connection.release()
        except Exception as e:
            logger.error('Release Queue: %s' % e)


class ConsumerQueue(kombu.mixins.ConsumerMixin):

    def __init__(self, uri, name, prefetch_count=100):
        '''
        Sample Consumer receiver message from queue
        Args:
            uri: list of uri connections.
            name: queue name.
            prefetch_count: prefetch count.
        Examples:
            >>> ConsumerQueue(uri=['amqp://username:password@host:5672/'],
            ... name='ExampleQueue',
            ... prefetch_count=100)
        '''

        self.queue_connection = QueueConnection(uri)
        self.queue_connection.connect()

        self.connection = self.queue_connection._connection

        self.queue = kombu.Queue(name)

        self.prefetch_count = prefetch_count

    def get_consumers(self, Consumer, channel):
        consumer = Consumer(queues=[self.queue], callbacks=[self.on_message_received])
        consumer.qos(prefetch_count=self.prefetch_count)
        return [consumer,]

    def on_message_received(self, payloads, messages):
        try:
            # do something with payloads
            process_successfully = True

            if process_successfully:
                messages.ack()
            else:
                messages.requeue()
        except Exception as e:
            logger.error('Message received: %s' % e)

            messages.requeue()