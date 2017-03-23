__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from processor import TwitterSpout
from apps.log_app import LogApp

chain_processor = ChainProcessor()
_twitter_spout = TwitterSpout({'consumer_secret': 'CONSUMER_SECRET', 'access_token': 'ACCESS_TOKEN', 'consumer_key': 'CONSUMER_KEY', 'access_token_secret': 'ACCESS_TOKEN_SECRET'})
_log_app = LogApp()
chain_processor.add_processor(_twitter_spout)
chain_processor.add_processor(_log_app)
_twitter_spout.run(chain_processor.process)