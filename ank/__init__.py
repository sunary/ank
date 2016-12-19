__author__ = 'sunary'

VERSION = '1.2.0'
API_DEFAULT_PORT = '5372'

from apps import app, api_app, schedule_app
from chains import chain_processor, join_processor, split_processor, log_handle
from chains import kafka_consumer, kafka_producer, rabbitmq_consumer, rabbitmq_producer, zmq_consumer, zmq_producer
# from deploy import dependency_injection, generate_processor, generate_setting
from queues import rabbit_mqueue
from utilities import my_cmd, my_api, my_deploy, my_helper, my_mongo