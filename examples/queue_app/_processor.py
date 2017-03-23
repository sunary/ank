__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from apps.rabbitmq_consumer import RabbitmqConsumer
from apps.log_app import LogApp
from processor import ExampleApp
from app.rabbitmq_consumer import RabbitmqProducer

chain_processor = ChainProcessor()
_rabbitmq_consumer = RabbitmqConsumer({'queue': 'ExampleQueue', 'uri': 'amqp://guest:guest@localhost:5672'})
_log_app = LogApp()
_example_app = ExampleApp()
_rabbitmq_producer = RabbitmqProducer({'exchange': 'ExampleExchange', 'uri': 'amqp://guest:guest@localhost:5672', 'routing_key': 'ExchangeToQueue'})
chain_processor.add_processor(_rabbitmq_consumer)
chain_processor.add_processor(_log_app)
chain_processor.add_processor(_example_app)
chain_processor.add_processor(_rabbitmq_producer)
_rabbitmq_consumer.run(chain_processor.process)