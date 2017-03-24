__author__ = 'sunary'


from base_apps.pipe_app import PipeApp


class FirstApp(PipeApp):

    def init_app(self, mongo=None, redis=None, batch_size=None):
        self.mongo = mongo
        self.redis = redis
        self.batch_size = batch_size

    def start(self):
        print('Start chain')
        for i in range(100):
            print '---start'
            self.chain_process({'content': i})
            print '---end'

    def process(self, message=None):
        print('start app {}'.format(message))
        return message


class PrintApp(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From print app')

    def process(self, message=None):
        print('print only {}'.format(message))
        return message


class ConditionalApp(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From conditional app')

    def process(self, message=None):
        print('condition check {}'.format(message))

        if message['content'] % 2:
            message.update({'flags': [False, True]})
        else:
            message.update({'flags': [True, False]})

        return message


class OddApp(PipeApp):

    def init_app(self, *agrs):
        pass

    def run(self, process=None):
        print('From odd app')

    def process(self, message=None):
        print('odd {}'.format(message))
        message['content'] = (message['content'] + 1)/2
        return message


class EvenApp(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From even app')

    def process(self, message=None):
        print('even {}'.format(message))
        message['content'] /= 2
        return message