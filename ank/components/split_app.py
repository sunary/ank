__author__ = 'sunary'


from ank.components.pipe_app import PipeApp


class SplitApp(PipeApp):

    def init_app(self):
        pass

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        return message
