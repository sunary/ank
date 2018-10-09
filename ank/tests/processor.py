__author__ = 'sunary'


from ank.core.app import App


class ConsumerApp(App):

    def __init__(self):
        self.range_from = 0
        self.range_to = 0

    def init_app(self, range_from=0, range_to=0):
        self.range_from = range_from
        self.range_to = range_to

    def start(self):
        print('Start chain')
        for i in range(self.range_from, self.range_to):
            self.execute(i)


class AdditionApp(App):

    def init_app(self, *args):
        pass

    def execute(self, message):
        return message + 5


class PrintApp(App):

    def init_app(self, *args):
        pass

    def execute(self, message):
        print(message)
        return message
