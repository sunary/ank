__author__ = 'sunary'


from apps._app import App
try:
    from kafka import KafkaConsumer
except:
    raise 'kafka not founded'


class KafkaAnkConsumer(App):
    '''
    Messages were received from consumer.subscribe
    '''

    def __init__(self, queue_config, topic):
        super(KafkaAnkConsumer, self).__init__()

        self.consumer = KafkaConsumer(queue_config)
        self.topic = topic

    def run(self, process=None):
        super(KafkaAnkConsumer, self).run(process)

        self.consumer.subscribe(self.topic)

        for message in self.consumer:
            self._process(message)

    def process(self, messages=None):
        return messages