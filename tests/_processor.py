__author__ = 'ank_generator'

from chains.chain_processor import ChainProcessor
from processor import TestApp
from utilities.my_mongo import Mongodb
from redis.client import StrictRedis
from chains.join_processor import JoinProcessor
from chains.log_handle import LogHandle
from processor import OtherApp
from chains.split_processor import SplitProcessor

chain_processor = ChainProcessor()
_mongodb = Mongodb('raw_data', 'twitter', 'localhost', 27017)
_strict_redis = StrictRedis('localhost', 6379)
_test_app = TestApp(_mongodb, _strict_redis, 2)
_join_processor = JoinProcessor(2)
_log_handle = LogHandle()
_other_app = OtherApp()
_split_processor = SplitProcessor()
chain_processor.add_processor(_test_app)
chain_processor.add_processor(_join_processor)
chain_processor.add_processor(_log_handle)
chain_processor.add_processor(_other_app)
chain_processor.add_processor(_split_processor)
_test_app.run(chain_processor.process)