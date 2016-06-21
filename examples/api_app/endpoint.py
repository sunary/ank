__author__ = 'sunary'


from apps.api_app import APIApp
from utils import my_api


class ExampleAPI(APIApp):
    '''
    Examples:
        localhost:15372/add?a=1&b=2
        localhost:15372/sub?a=5&b=3
    '''
    def add(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a + b))

    def sub(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return my_api.success(message=str(a - b))