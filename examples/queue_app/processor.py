__author__ = 'sunary'


from base_apps.pipe_app import PipeApp


class ExampleApp(PipeApp):

    def init_app(self):
        pass

    def start(self):
        pass

    def process(self, messages=None):
        print(messages)

        return messages