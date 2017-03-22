__author__ = 'ank_generator'

from deploy.chain_processor import ChainProcessor
from processor import ScheduleExample

chain_processor = ChainProcessor()
_schedule_example = ScheduleExample('0 0 * * 5', True)
chain_processor.add_processor(_schedule_example)
_schedule_example.run(chain_processor.process)