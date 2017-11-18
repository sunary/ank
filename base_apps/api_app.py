__author__ = 'sunary'


import os
from base_apps.pipe_app import PipeApp
from flask import Flask
from utilities import my_api


def is_production():
    return os.environ.get('ENV', 'dev').lower == 'production'

class APIApp(PipeApp):
    '''
    API App
    Add function to extend class to create new API
    '''

    def init_app(self, host='localhost', port=5372, **kwargs):
        self.host = host
        self.port = port

    def start(self):
        flask_app = Flask(__name__)

        @flask_app.route('/')
        def index():
            return 'Welcome!'

        @my_api.crossdomain(origin='*')
        @flask_app.route('/<method>', methods=['GET', 'POST'])
        def _(method):
            try:
                params = my_api.get_options()
                method = getattr(self, method)
                return method(params)
            except Exception as e:
                self.logger.error(e)

                return my_api.failed(return_json={'detail': str(e)}, status_code=404,
                                     message='The requested url does not exist')

        flask_app.run(host=self.host, port=self.port, debug=not is_production())