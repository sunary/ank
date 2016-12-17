__author__ = 'sunary'


from apps.app import BaseApp


class JoinProcessor(BaseApp):
    '''
    Join messages from previous processor
    '''
    def __init__(self, batch_size=100):
        super(JoinProcessor, self).__init__()

        self.batch_size = batch_size
        self.messages = []

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):

        return messages