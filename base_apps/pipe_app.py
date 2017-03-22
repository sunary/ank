__author__ = 'sunary'


from utilities import my_helper


class PipeApp(object):

    '''
    Start app from run() method
    Process message in process() method
    '''

    def __init__(self, *args, **kwargs):
        self.logger = my_helper.init_logger(self.__class__.__name__)

        self.init_app(*args, **kwargs)

    def init_app(self):
        pass

    def run(self, process=None):
        self.chain_process = process or self.process

        self.start()

    def start(self):
        '''
        Your self.process become self.chain_process. Start run everything from it
        '''
        pass

    def process(self, message=None):

        return message