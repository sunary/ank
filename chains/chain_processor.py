__author__ = 'sunary'


from utilities import my_helper
import copy


class ChainProcessor(object):
    '''
    Run chain processors
    Output of a processor will be input of the next processor
    '''

    def __init__(self):
        self.logger = my_helper.init_logger(self.__class__.__name__)

        self.methods = []

    def run(self):
        self.methods[0][0].run(self.process())

    def add_processor(self, processor, method='process'):
        self.methods.append((processor, getattr(processor, method)))

    def process(self, messages=None):
        for i, mth in enumerate(self.methods):
            processor, method = mth
            try:
                processor_name = processor.__class__.__name__
                self.logger.info('Run processor: {}'.format(processor_name))

                if processor_name == 'JoinProcessor':
                    processor.messages.append(messages)
                    if len(processor.messages) >= processor.batch_size:
                        messages = method(processor.messages)
                        processor.messages = []
                    else:
                        return None
                elif processor_name == 'SplitProcessor':
                    _messages = copy.deepcopy(messages)
                    for msg in _messages:
                        messages = method(msg)
                else:
                    messages = method(messages)

            except Exception as e:
                self.logger.error('Error when run process {}: {}'.format(processor_name, e))
                raise Exception('Error when run process {}: {}'.format(processor_name, e))

        return messages