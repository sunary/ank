__author__ = 'sunary'


from ank.core.app import App


class LogApp(App):

    def init_app(self):
        pass

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.logger.info(message)
        return message
