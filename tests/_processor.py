__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from processor import FirstApp
from utilities.my_mongo import Mongodb
from redis.client import StrictRedis
from apps.join_app import JoinApp
from apps.log_app import LogApp
from processor import SecondApp
from apps.split_app import SplitApp
from processor import ConditionalWorker
from processor import ThirdApp
from processor import OtherApp

chain_processor = ChainProcessor()
_mongodb = Mongodb('raw_data', 'twitter', 'localhost', 27017)
_strict_redis = StrictRedis('localhost', 6379)
_first_app = FirstApp(_mongodb, _strict_redis, 2)
_join_app = JoinApp(2)
_log_app = LogApp()
_second_app = SecondApp()
_split_app = SplitApp()
_conditional_worker = ConditionalWorker()
_third_app = ThirdApp()
_other_app = OtherApp()
chain_processor.add_processor(_first_app)
chain_processor.add_processor(_join_app)
chain_processor.add_processor(_log_app)
chain_processor.add_processor(_second_app)
chain_processor.add_processor(_split_app)
chain_processor.add_processor(_conditional_worker)
chain_processor.add_processor([_third_app, _other_app])
chain_processor.add_processor(_log_app)
_first_app.run(chain_processor.process)