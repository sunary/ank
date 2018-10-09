__author__ = 'sunary'


from ank.utils import logger


class App(object):
    """
    Start app from run() method
    Process message in process() method
    """

    def __init__(self, *args, **kwargs):
        self.logger = logger.init_logger(self.__class__.__name__)

        self.init_app(*args, **kwargs)

    def init_app(self, *args, **kwargs):
        pass

    def run(self):
        self.start()

    def start(self):
        """
        Your self.process become self.chain_process
        Start run everything from it
        """

    def execute(self, message):
        return message
