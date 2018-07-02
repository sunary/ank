__author__ = 'sunary'


from ank.apps.pipe_app import PipeApp


class LogApp(PipeApp):

    def init_app(self):
        pass

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.logger.info(message)
        return message
