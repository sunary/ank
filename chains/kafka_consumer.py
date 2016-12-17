__author__ = 'sunary'


from apps.app import BaseApp


class KafkaAnkConsumer(BaseApp):
    '''
    Messages were received from consumer.subscribe
    '''

    def __init__(self, consumer, topic):
        '''
        Args:
            consumer: kafka.KafkaConsumer
            topic: subscriber topic
        '''
        super(KafkaAnkConsumer, self).__init__()

        self.consumer = consumer
        self.topic = topic

    def run(self, process=None):
        super(KafkaAnkConsumer, self).run(process)

        self.consumer.subscribe(self.topic)

        for message in self.consumer:
            self._process(message)

    def process(self, messages=None):

        return messages