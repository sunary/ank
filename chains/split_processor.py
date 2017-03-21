__author__ = 'sunary'


from apps.app import BaseApp


class SplitProcessor(BaseApp):

    def __init__(self):
        super(SplitProcessor, self).__init__()

    def run(self, process=None):
        self.logger.info('Start {}'.format(self.__name__))

    def process(self, message=None):

        return message