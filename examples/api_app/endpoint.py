__author__ = 'sunary'


from ank.base_apps.api_app import APIApp
from ank.utils import api_helpers


class ExampleAPI(APIApp):

    def init_app(self, host='localhost', port=5372):
        pass

    # path: host:port/api/add?a=1&b=2
    def add(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        return api_helpers.success(message=str(a + b))

    # path: host:port/api/sub?x=105&y=17
    def sub(self, params):
        x = int(params.get('x'))
        y = int(params.get('y'))
        return api_helpers.success(message=str(x - y))