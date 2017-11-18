__author__ = 'sunary'


from base_apps.pipe_app import PipeApp
try:
    import zmq
except:
    raise Exception('pyzqm not found')


class ZeroMqConsumer(PipeApp):
    '''
    Message was received from sock.recv
    '''

    def init_app(self, uri=None, topic=None):
        context = zmq.Context()

        self.sock = context.socket(zmq.PULL)
        self.sock.bind(uri)
        self.sock.setsockopt(zmq.PULL, topic)

    def start(self):
        while True:
            message = self.sock.recv()
            self.chain_process(message)

    def process(self, message=None):
        return message