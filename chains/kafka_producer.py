__author__ = 'sunary'


from apps.app import BaseApp


class KafkaAnkProducer(BaseApp):
    '''
    Push message to queue
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

    def process(self, message=None):
        self.producer.send(self.topic, message)

        return message