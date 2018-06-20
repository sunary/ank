__author__ = 'sunary'


from endpoint import ExampleAPI
from ank.base_apps.pipe_app import PipeApp


class ExampleApp(PipeApp):

    def init_app(self, mongo):
        self.mongo = mongo

    def start(self):
        api_app = ExampleAPI(host='localhost', port=5372)
        api_app.run()