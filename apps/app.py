__author__ = 'sunary'


from utilities import my_helper


class BaseApp(object):

    '''
    Start app from run() method
    Process message in process() method
    '''

    def __init__(self):
        self.logger = my_helper.init_logger(self.__class__.__name__)

    def run(self, process=None):
        self._process = process or self.process

    def process(self, message=None):

        return message