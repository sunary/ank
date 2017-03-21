__author__ = 'sunary'


from apps.app import BaseApp


class FirstApp(BaseApp):

    def __init__(self, mongo, redis, batch_size, *args):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        super(FirstApp, self).run(process)

        print('Start chain')
        for i in range(100):
            self._process((i, i + 1))

    def process(self, message=None):
        print('Demo worker {}'.format(message))
        return message


class SecondApp(BaseApp):

    def __init__(self, *args):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        print('From 2nd worker')

    def process(self, message=None):
        print('After join {}'.format(message))
        return message


class ConditionalWorker(BaseApp):

    def __init__(self, *args):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        print('From conditional worker')

    def process(self, message=None):
        print('After split {}'.format(message))
        return message, (False, True)


class ThirdApp(BaseApp):

    def __init__(self, *agrs):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        print('From 3rd worker')

    def process(self, message=None):
        print('3rd worker {}'.format(message))
        return str(message) + ' pass ThirdApp'


class OtherApp(BaseApp):

    def __init__(self, *args):
        super(BaseApp, self).__init__()

    def run(self, process=None):
        print('From other worker')

    def process(self, message=None):
        print('Never pass 3rd worker {}'.format(message))
        return str(message) + ' pass OtherApp'