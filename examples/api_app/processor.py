__author__ = 'sunary'


from endpoint import ExampleAPI
from ank.components.pipe_app import PipeApp


class ExampleApp(PipeApp):

    def init_app(self, mongo_client=None):
        self.mongo = mongo_client

    def start(self):
        api_app = ExampleAPI(host='localhost', port=5372, mongo_client=self.mongo, mongo_db='demo')
        api_app.run()
