__author__ = 'sunary'


from apps.app import BaseApp


class LogHandle(BaseApp):

    def __init__(self):
        super(LogHandle, self).__init__()

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        self.logger.info(messages)
        return messages