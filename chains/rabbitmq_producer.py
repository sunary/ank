__author__ = 'sunary'


from apps._app import App
from queue.queue import Queue


class RabbitMqProducer(App):
    '''
    Post message(s) to queue
    '''
    def __init__(self, config):
        super(RabbitMqProducer, self).__init__()

        self.queue = Queue(config)

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        if messages:
            self.queue.post(messages)

        return messages