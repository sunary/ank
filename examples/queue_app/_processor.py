__author__ = 'ank'

from chains.chain_processor import ChainProcessor
from chains.get_message import GetMessage
from chains.log_handle import LogHandle
from processor import ExampleApp

chain_processor = ChainProcessor()
_get_message = GetMessage({'queue_config': {'uri': ['amqp://username:password@host:5672/'], 'name': 'ExampleQueue'}, 'batch_size': 100})
_log_handle = LogHandle()
_example_app = ExampleApp()
chain_processor.add_processor(_get_message)
chain_processor.add_processor(_log_handle)
chain_processor.add_processor(_example_app)
_get_message.run(chain_processor.process)