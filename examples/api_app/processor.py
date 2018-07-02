__author__ = 'sunary'


from endpoint import ExampleAPI
from ank.apps.pipe_app import PipeApp


class ExampleApp(PipeApp):

    def __init__(self, agrs, **kwagrs):
        super(ExampleApp, self).__init__()

    def start(self):
        api_app = ExampleAPI(host='localhost', port=5372, mongo_client=self.mongo, mongo_db='demo')
        api_app.run()
