__author__ = 'sunary'


from ank.apps.pipe_app import PipeApp
try:
    import zmq
except ImportError:
    raise ImportError('pyzqm not found')


class ZeroMqConsumer(PipeApp):
    """
    Message was received from sock.recv
    """

    def init_app(self, uri='', topic=''):
        """
            Args:
                uri (string): connection uri
                topic (string): topic name
        """
        context = zmq.Context()

        self.sock = context.socket(zmq.PULL)
        self.sock.bind(uri)
        self.topic = topic

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))
        self.sock.setsockopt(zmq.PULL, self.topic)
        while True:
            message = self.sock.recv()
            self.chain_process(message)

    def process(self, message=None):
        return message
