__author__ = 'sunary'


from utils import my_helper


class App(object):

    '''
    start app from run() method
    receive messages or start process from on_messages_received() method
    process message(s) in process() method
    '''

    def __init__(self):
        self.logger = my_helper.init_logger(self.__class__.__name__)

    def run(self, process=None):
        self._process = process or self.process

    def on_messages_received(self, messages=None):

        return messages

    def process(self, messages=None):

        return messages