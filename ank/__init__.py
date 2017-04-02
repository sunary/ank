__author__ = 'sunary'


VERSION = '1.4.3'
API_DEFAULT_PORT = '5372'


from base_apps import pipe_app, api_app, schedule_app
from apps import join_app, split_app, log_app
from apps import kafka_consumer, kafka_producer, rabbitmq_consumer, rabbitmq_producer, zmq_consumer, zmq_producer
from deploy import chain_processor
# from deploy import dependency_injection, generate_processor, generate_setting
from utilities import my_cmd, my_api, my_deploy, my_helper, my_mongo