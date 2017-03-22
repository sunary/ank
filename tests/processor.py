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
            self.chain_process((i, i + 1))

    def process(self, message=None):
        print('Demo worker {}'.format(message))
        return message


class SecondApp(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From 2nd worker')

    def process(self, message=None):
        print('After join {}'.format(message))
        return message


class ConditionalWorker(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From conditional worker')

    def process(self, message=None):
        print('After split {}'.format(message))
        return message, (False, True)


class ThirdApp(PipeApp):

    def init_app(self, *agrs):
        pass

    def run(self, process=None):
        print('From 3rd worker')

    def process(self, message=None):
        print('3rd worker {}'.format(message))
        return str(message) + ' pass ThirdApp'


class OtherApp(PipeApp):

    def init_app(self, *args):
        pass

    def run(self, process=None):
        print('From other worker')

    def process(self, message=None):
        print('Never pass 3rd worker {}'.format(message))
        return str(message) + ' pass OtherApp'