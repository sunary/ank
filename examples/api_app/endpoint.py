__author__ = 'sunary'


from base_apps.api_app import APIApp
from utilities import my_api


class ExampleAPI(APIApp):

    def init_app(self, host='localhost', port=5372):
        pass

    def add(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a + b))

    def sub(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a - b))