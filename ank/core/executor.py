__author__ = 'sunary'


from ank.utils import logger
import collections


class Executor(object):
    """
    Run chain processors
    Output of a processor will be input of the next processor
    """

    def __init__(self):
        self.logger = logger.init_logger(self.__class__.__name__)

        self.processors = []

    def run(self):
        if self.processors:
            self.processors[0].run()
        else:
            self.logger.error('ValueError: processors empty')
            raise ValueError('processors empty')

    def add_processor(self, dependency_processor):
        """
        add dependency_processor
        """
        self.processors.append(dependency_processor)

    def execute(self, message, next_processors=None):
        """
        Execute chain dependency_processor
        """
        next_processors = next_processors or self.processors

        for i, processor in enumerate(next_processors):
            processor_name = processor.class_name()

            if processor_name == 'SplitApp':
                if isinstance(message, collections.Iterable):
                    next_processors = next_processors[i + 1:]
                    for msg in message:
                        self.execute(msg, next_processors)
                    return None
                else:
                    self.logger.error('ValueError: message in `SplitApp` must be Iterable')
                    raise ValueError('message in `SplitApp` must be Iterable')
            else:
                message = processor.execute(message)

        return message
