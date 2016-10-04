__author__ = 'sunary'


from apps._app import App
try:
    import zmq
except:
    raise Exception('not founded pyzmq')


class ZeroMqProducer(App):
    '''
    Push message(s) to queue
    '''

    def __init__(self, uri, topic):
        super(ZeroMqProducer, self).__init__()

        context = zmq.Context()

        self.sock = context.socket(zmq.PUSH)
        self.sock.bind(uri)
        self.sock.setsockopt(zmq.PULL, topic)

    def process(self, messages=None):
        self.sock.send(messages)

        return messages