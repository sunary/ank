__author__ = 'sunary'


from ank.apps.pipe_app import PipeApp


class FirstApp(PipeApp):

    def init_app(self, redis=None, range_from=0, range_to=0):
        self.redis = redis
        self.range_from = range_from
        self.range_to = range_to

    def start(self):
        redis_key = 'redis_key'
        self.redis.set(redis_key, 'hello world')
        print('Message from redis: {}'.format(self.redis.get(redis_key)))

        print('Start chain')
        for i in range(self.range_from, self.range_to):
            print('---start')
            self.chain_process({'content': i})
            print('---end')

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
