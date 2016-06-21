__author__ = 'sunary'


from apps._app import App


class SplitProcessor(App):

    def __init__(self):
        super(SplitProcessor, self).__init__()

    def run(self, process=None):
        self.logger.info('Start ...')

    def process(self, messages=None):
        self.logger.info('Split')
        return messages