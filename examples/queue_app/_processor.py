__author__ = 'ank_generator'

from chains.chain_processor import ChainProcessor
from chains.rabbitmq_consumer import RabbitMqConsumer
from chains.log_handle import LogHandle
from chains.rabbitmq_producer import RabbitMqProducer
from processor import ExampleApp

chain_processor = ChainProcessor()
_rabbit_mq_message = RabbitMqConsumer(uri=['amqp://username:password@host:5672/'], name='ExampleQueue', batch_size=100)
_log_handle = LogHandle()
_example_app = ExampleApp()
_rabbit_mq_producer = RabbitMqProducer(uri=['amqp://username:password@host:5672/'], name='ExampleExchange')
chain_processor.add_processor(_rabbit_mq_message)
chain_processor.add_processor(_log_handle)
chain_processor.add_processor(_example_app)
chain_processor.add_processor(_rabbit_mq_producer)
_rabbit_mq_message.run(chain_processor.process)