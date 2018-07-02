__author__ = 'sunary'


from ank.utils import logger


class PipeApp(object):
    """
    Start app from run() method
    Process message in process() method
    """

    def __init__(self, *args, **kwargs):
        self.logger = logger.init_logger(self.__class__.__name__)

        self.init_app(*args, **kwargs)

    def init_app(self, *args, **kwargs):
        pass

    def run(self, process=None):
        self.chain_process = process or self.process

        self.start()

    def start(self):
        """
        Your self.process become self.chain_process
        Start run everything from it
        """

    def process(self, message=None):
        """
        Args:
            message: {'content': (*) 'content of message',
                      'flags': (list|tuple) 'define next process will be use'}
                          raise TypeError if you don't declare this in return of before branching-processor
                          if 'flags' == [True, True]: process both in next branching-processors
                          if 'flags' == [True, False]: process 1st processor in next branching-processors
                          if 'flags' == [False, True]: process 2nd processor in next branching-processors
                          if 'flags' == [False, False]: no processor, stop chain
                      is None: stop chain
        """
        return message
