__author__ = 'sunary'


from apps.app import BaseApp
from flask import Flask
from utilities import my_api


class APIApp(BaseApp):
    '''
    API App
    Add function to extend class to create new API
    '''

    def __init__(self, host='localhost', port=5372, **kwargs):
        super(APIApp, self).__init__()

        self.host = host
        self.port = port

    def run(self, process=None):
        super(APIApp, self).run(process)

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

        flask_app.run(host=self.host, port=self.port, debug=True)