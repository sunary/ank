__author__ = 'sunary'


from ank.base_apps.api_app import APIApp


class ExampleAPI(APIApp):

    def init_app(self, host='localhost', port=5372, mongo_client=None, mongo_db=''):
        self.db = mongo_client[mongo_db]

    # path: host:port/api/add?a=1&b=2
    def add(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        result = a + b

        collection = self.db['add']
        collection.insert({'param1': a, 'param2': b, 'result': result})
        return {'result': result}

    # path: host:port/api/sub?a=105&b=17
    def sub(self, params):
        a = int(params.get('a'))
        b = int(params.get('b'))
        result = a - b

        collection = self.db['sub']
        collection.insert({'param1': a, 'param2': b, 'result': result})
        return {'result': result}