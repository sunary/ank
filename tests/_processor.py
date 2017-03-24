__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from processor import FirstApp
from utilities.my_mongo import Mongodb
from redis.client import StrictRedis
from apps.join_app import JoinApp
from apps.split_app import SplitApp
from processor import ConditionalApp
from processor import EvenApp
from processor import OddApp
from processor import PrintApp

chain_processor = ChainProcessor()
_mongodb = Mongodb('raw_data', 'twitter', 'localhost', 27017)
_strict_redis = StrictRedis('localhost', 6379)
_first_app = FirstApp(_mongodb, _strict_redis, 2)
_join_app = JoinApp(2)
_split_app = SplitApp()
_conditional_app = ConditionalApp()
_even_app = EvenApp()
_odd_app = OddApp()
_print_app = PrintApp()
chain_processor.add_processor(_first_app)
chain_processor.add_processor(_join_app)
chain_processor.add_processor(_split_app)
chain_processor.add_processor(_conditional_app)
chain_processor.add_processor([_even_app, _odd_app])
chain_processor.add_processor(_print_app)
_first_app.run(chain_processor.process)