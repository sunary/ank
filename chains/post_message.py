__author__ = 'sunary'


from apps._app import App
from queue.queue import Queue


class PostMessage(App):
    '''
    Join messages from previous processor
    '''
    def __init__(self, config):
        super(PostMessage, self).__init__()

        self.queue = Queue(config)

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        if messages:
            self.queue.post(messages)