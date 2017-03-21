__author__ = 'sunary'


from apps.app import BaseApp
try:
    import zmq
except ImportError:
    raise ImportError('No module named zmq')


class ZeroMqProducer(BaseApp):
    '''
    Push message to queue
    '''

    def __init__(self, uri, topic):
        super(ZeroMqProducer, self).__init__()

        context = zmq.Context()

        self.sock = context.socket(zmq.PUSH)
        self.sock.bind(uri)
        self.sock.setsockopt(zmq.PULL, topic)

    def process(self, message=None):
        self.sock.send(message)

        return message