__author__ = 'ank_generator'

from chains.chain_processor import ChainProcessor
from processor import TwitterSpout
from chains.log_handle import LogHandle

chain_processor = ChainProcessor()
_twitter_spout = TwitterSpout({'consumer_secret': 'l4aedMD8n5CFEvmNK33Ivgqg6HtF2xyC0mLjqsunK7dq5dG6t3', 'access_token': '111489227-jaCTEYzhNNQiazks9wMvqkvssYfg8UVZfLoHpTQX', 'consumer_key': 'PnJWVNheDV0sYxBhdSIYk4aiG', 'access_token_secret': 'nUJ2q3t1KhWBlvN32CjoSBCTMiAmvGy68eFmnq1my0a8m'})
_log_handle = LogHandle()
chain_processor.add_processor(_twitter_spout)
chain_processor.add_processor(_log_handle)
_twitter_spout.run(chain_processor.process)