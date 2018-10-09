__author__ = 'sunary'


from ank.core.app import App


class JoinApp(App):
    """
    Join messages from previous processor
    """

    def __init__(self):
        self.batch_size = 0

    def init_app(self, batch_size=None):
        self.batch_size = batch_size

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        return message
