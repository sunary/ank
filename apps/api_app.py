__author__ = 'sunary'


from ._app import App
from flask import Flask
from utils import my_api


class APIApp(App):
    '''
    API App
    Add function to extend class to create new API
    '''

    def __init__(self, host='localhost', port=15372):
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