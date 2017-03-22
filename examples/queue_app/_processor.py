__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from apps.rabbitmq_consumer import RabbitmqConsumer
from apps.log_app import LogApp
from apps.rabbitmq_producer import RabbitmqProducer
from processor import ExampleApp

chain_processor = ChainProcessor()
_rabbit_mq_message = RabbitmqConsumer(uri='amqp://username:password@host:5672/', name='ExampleQueue', batch_size=100)
_log_handle = LogApp()
_example_app = ExampleApp()
_rabbit_mq_producer = RabbitmqProducer(uri='amqp://username:password@host:5672/', exchange='ExampleExchange', routing_key='ExchangeToQueue')
chain_processor.add_processor(_rabbit_mq_message)
chain_processor.add_processor(_log_handle)
chain_processor.add_processor(_example_app)
chain_processor.add_processor(_rabbit_mq_producer)
_rabbit_mq_message.run(chain_processor.process)