__author__ = 'sunary'


from apps.app import BaseApp


class ExampleApp(BaseApp):

    def __init__(self):
        super(ExampleApp, self).__init__()

    def run(self, process=None):
        super(ExampleApp, self).run(process)

    def process(self, messages=None):
        print(messages)

        return messages