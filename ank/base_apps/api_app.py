__author__ = 'sunary'


import os
from ank import API_DEFAULT_PORT
from ank.base_apps.pipe_app import PipeApp
try:
    from flask import Flask
except ImportError:
    ImportError('flask not found')
from ank.utils import api_helpers


def is_production():
    return os.environ.get('ENV', 'dev').lower == 'production'


class APIApp(PipeApp):
    """
    API App
    Add function to extend class to create new API
    """

    def init_app(self, host='localhost', port=API_DEFAULT_PORT):
        """
        Args:
             host (string): RestAPI host, default 'localhost'
             port (int): RestAPI host, default API_DEFAULT_PORT=5372
        """
        self.host = host
        self.port = port

    def start(self):
        flask_app = Flask(__name__)

        @flask_app.route('/')
        def index():
            return 'Hello world!'

        @api_helpers.crossdomain(origin='*')
        @flask_app.route('/api/<method>', methods=['GET', 'POST'])
        def _(method):
            try:
                params = api_helpers.get_options()
                method = getattr(self, method)
                return method(params)
            except Exception as e:
                self.logger.error(e)

                return api_helpers.failed(return_json={'detail': str(e)}, status_code=404,
                                          message='The requested url does not exist')

        flask_app.run(host=self.host, port=self.port, debug=not is_production())
