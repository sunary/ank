__author__ = 'ank'

from chains.chain_processor import ChainProcessor
from processor import TestApp
from utilities.my_mongo import Mongodb
from redis.client import StrictRedis
from chains.join_processor import JoinProcessor
from chains.log_handle import LogHandle
from processor import OtherApp

chain_processor = ChainProcessor()
_mongodb = Mongodb('raw_data', 'twitter', 'localhost', 27017)
_strict_redis = StrictRedis('localhost', 6379)
_test_app = TestApp(_mongodb, _strict_redis, 2)
_join_processor = JoinProcessor(2)
_log_handle = LogHandle()
_other_app = OtherApp()
chain_processor.add_processor(_test_app)
chain_processor.add_processor(_join_processor)
chain_processor.add_processor(_log_handle)
chain_processor.add_processor(_other_app)
_test_app.run(chain_processor.process)