__author__ = 'sunary'


from apps.app import BaseApp


class TestApp(BaseApp):

    def __init__(self, mongo, redis, batch_size, *wagrs):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        super(TestApp, self).run(process)

        print('Start chain')
        for i in range(100):
            self._process((i, i + 1))

    def process(self, message=None):
        print('Demo worker {}'.format(message))
        return message


class OtherApp(BaseApp):

    def __init__(self, *wagrs):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        print('From other worker')

    def process(self, message=None):
        print('Other worker {}'.format(message))
        return None