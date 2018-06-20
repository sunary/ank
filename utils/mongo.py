__author__ = 'sunary'


try:
    from pymongo import MongoClient, ReturnDocument
except ImportError:
    raise ImportError('pymongo not found')


class Mongodb(object):

    def __init__(self, db, col, host='127.0.0.1', port=27017, username=None, password=None):
        if username and password:
            self._client = MongoClient('mongodb://{0}:{1}@{2}:{3}/{4}?authMechanism=SCRAM-SHA-1'.format(
                    username, password, host, port, db))
        else:
            self._client = MongoClient(host, port)
            # if username and password:
            #     self._client[db].authenticate(username, password, mechanism='SCRAM-SHA-1')

        if isinstance(col, (tuple, list)):
            self.cols_accept = col
            col = self.cols_accept[0]
        else:
            self.cols_accept = None

        self._db = self._client[db]
        self.collection = self._db[col]

    def change_collection(self, col_name):
        if self.cols_accept and col_name not in self.cols_accept:
            raise Exception('new collection is not registered')

        self.collection = self._db[col_name]

    def find(self, spec={}, select=[], limit=0, skip=0, chunk_size=500, sort=None, **kwargs):
        if limit:
            cur = self.collection.find(
                    filter=spec,
                    projection=select,
                    skip=skip,
                    limit=limit,
                    **kwargs
                )

            if sort:
                cur = cur.sort(sort)

            for each in cur:
                yield each
        else:
            while True:
                cur = self.collection.find(
                    filter=spec,
                    projection=select,
                    skip=skip,
                    limit=chunk_size,
                    **kwargs
                )
                if sort:
                    cur = cur.sort(sort)

                if cur.count(True) == 0:
                    break
                for each in cur:
                    yield each
                    skip += 1

    def find_one(self, spec={}, select=None, skip=0, sort=None):
        return self.collection.find_one(filter=spec,
                                        projection=select,
                                        skip=skip,
                                        sort=None)

    def insert(self, docs, **kwargs):
        return self.collection.insert(doc_or_docs=docs, **kwargs)

    def update(self, spec, doc, **kwargs):
        if doc.get('$set'):
            return self.collection.update(spec, doc, **kwargs)['nModified']

        return self.collection.update(spec, {'$set': doc}, **kwargs)['nModified']

    def batch_update(self, spec, docs, **kwargs):
        bulk = self.collection.initialize_unordered_bulk_op()
        for i in range(len(docs)):
            bulk.find(spec[i]).update({'$set': docs[i]})

        bulk.execute()

    def increase(self, spec, doc, **kwargs):
        if doc.get('$inc'):
            return self.collection.update(spec, doc, **kwargs)
        return self.collection.update(spec, {'$inc': doc}, **kwargs)

    def count(self, spec=None):
        return self.collection.find(spec).count()

    def remove(self, spec=None):
        if spec is None:
            self.collection.remove()
        else:
            self.collection.remove(spec)

    def rename(self, new_name):
        self.collection.rename(new_name)

    def create_index(self, keys, **kwargs):
        self.collection.create_index(keys, **kwargs)

    def next_sequence(self, seq_name, col_sequence='counters', rtype=str):
        col_seq = self._db[col_sequence]
        res = col_seq.find_one_and_update({'_id': seq_name}, {'$inc': {'seq': 1}},
                                          upsert=True,
                                          full_response=True,
                                          return_document=ReturnDocument.AFTER)
        return rtype(res['seq'])

    def export_csv(self, fields, output):
        import pandas as pd

        result = []
        for doc in self.find(select=fields):
            result.append(doc)

        df = pd.DataFrame(data=result, columns=fields)
        df.to_csv(output, index=False, encoding='utf-8')

    def export_excel(self, fields, output):
        import pandas as pd

        result = []
        for doc in self.find(select=fields):
            result.append(doc)

        df = pd.DataFrame(data=result, columns=fields)
        df.to_excel(output, index=False, encoding='utf-8')
