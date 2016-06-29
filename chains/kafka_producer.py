__author__ = 'sunary'


from apps._app import App
try:
    from kafka import KafkaProducer
except:
    raise 'kafka-python not founded'


class KafkaAnkProducer(App):
    '''
    Post message(s) to queue
    '''

    def __init__(self, queue_config, topic):
        super(KafkaAnkProducer, self).__init__()

        self.producer = KafkaProducer(queue_config)
        self.topic = topic

    def process(self, messages=None):
        self.producer.send(self.topic, messages)

        return messages