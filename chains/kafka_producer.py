__author__ = 'sunary'


from apps.app import BaseApp


class KafkaAnkProducer(BaseApp):
    '''
    Push message(s) to queue
    '''

    def __init__(self, producer, topic):
        '''
        Args:
            producer: kafka.KafkaProducer
            topic: subscriber topic
        '''
        super(KafkaAnkProducer, self).__init__()

        self.producer = producer
        self.topic = topic

    def process(self, messages=None):
        self.producer.send(self.topic, messages)

        return messages