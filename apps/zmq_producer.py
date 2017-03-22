__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
try:
    import zmq
except ImportError:
    raise ImportError('No module named zmq')


class ZeroMqProducer(PipeApp):
    '''
    Push message to queue
    '''

    def init_app(self, uri=None, topic=None):
        context = zmq.Context()

        self.sock = context.socket(zmq.PUSH)
        self.sock.bind(uri)
        self.sock.setsockopt(zmq.PULL, topic)

    def start(self):
        self.logger.info('Start {}'.format(self.__class__.__name__))

    def process(self, message=None):
        self.sock.send(message)

        return message