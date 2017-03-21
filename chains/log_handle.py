__author__ = 'sunary'


from apps.app import BaseApp


class LogHandle(BaseApp):

    def __init__(self):
        super(LogHandle, self).__init__()

    def run(self, process=None):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.logger.info(message)

        return message