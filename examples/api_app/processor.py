__author__ = 'sunary'


from examples.api_app.endpoint import ExampleAPI
from apps._base_app import BaseApp


class ExampleApp(BaseApp):

    def __init__(self, mongo):
        pass

    def run(self, process=None):
        api_app = ExampleAPI(host='localhost', port=15372)
        api_app.run()