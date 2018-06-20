__author__ = 'sunary'


from base_apps.pipe_app import PipeApp


class KafkaAnkConsumer(PipeApp):
    """
    Message was received from consumer.subscribe
    """

    def ini_app(self, consumer=None, topic=None):
        """
        Args:
            consumer (kafka.KafkaConsumer): kafka consumer
            topic (string): kafka subscriber topic
        """
        self.consumer = consumer
        self.topic = topic

    def start(self):
        self.consumer.subscribe(self.topic)

        for message in self.consumer:
            self.chain_process(message)

    def process(self, message=None):
        return message
