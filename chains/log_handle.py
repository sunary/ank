__author__ = 'sunary'


from apps._app import App


class LogHandle(App):

    def __init__(self):
        super(LogHandle, self).__init__()

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        self.logger.info(messages)
        return messages