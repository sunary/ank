__author__ = 'ank'

from chains.chain_processor import ChainProcessor
from processor import ExampleApp
from utilities.my_mongo import Mongodb

chain_processor = ChainProcessor()
_mongodb = Mongodb('raw_data', 'twitter', 'localhost', 27017)
_example_app = ExampleApp(_mongodb)
chain_processor.add_processor(_example_app)
_example_app.run(chain_processor.process)