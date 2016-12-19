__author__ = 'sunary'


from apps.api_app import APIApp
from utilities import my_api


class ExampleAPI(APIApp):

    def __init__(self, host='localhost', port=5372):
        super(ExampleAPI, self).__init__(host, port)

    def add(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a + b))

    def sub(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a - b))