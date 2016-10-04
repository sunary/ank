__author__ = 'sunary'


from apps._app import App
try:
    import zmq
except:
    raise Exception('not founded pyzmq')


class ZeroMqConsumer(App):
    '''
    Messages were received from sock.recv
    '''

    def __init__(self, uri, topic):
        super(ZeroMqConsumer, self).__init__()

        context = zmq.Context()

        self.sock = context.socket(zmq.PULL)
        self.sock.bind(uri)
        self.sock.setsockopt(zmq.PULL, topic)

    def run(self, process=None):
        super(ZeroMqConsumer, self).run(process)

        while True:
            message = self.sock.recv()
            self._process(message)

    def process(self, messages=None):

        return messages