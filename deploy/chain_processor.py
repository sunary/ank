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
        '''
        add processor(s) and method(n) into chain
        '''
        if isinstance(processor, list):
            list_methods = []
            for proc in processor:
                list_methods.append(getattr(proc, method))

            self.methods.append((processor, list_methods))
        else:
            self.methods.append((processor, getattr(processor, method)))

    def process(self, message=None, chain_methods=None):
        '''
        Process chain depend methods registered
        '''
        _message = copy.deepcopy(message)
        chain_methods = chain_methods or self.methods

        for i, mthd in enumerate(chain_methods):
            if _message is None:
                return None

            processor, method = mthd
            if isinstance(processor, list):
                try:
                    _message, flags = _message
                except TypeError:
                    raise TypeError('message type must be tuple2: (message_value, flags)')

                if isinstance(flags, (tuple, list)):
                    for j, status in enumerate(flags):
                        if status:
                            processor_name = processor[j].__class__.__name__
                            self.logger.info('Run processor: {}'.format(processor_name))

                            try:
                                _message = method[j](_message)
                                break
                            except Exception as e:
                                self.logger.error('Error when run process {}: {}'.format(processor_name, e))
                                raise Exception('Error when run process {}: {}'.format(processor_name, e))
                else:
                    processor_name = processor[j].__class__.__name__
                    self.logger.info('Run processor: {}'.format(processor_name))
                    try:
                        _message = method[0](_message)
                    except Exception as e:
                        self.logger.error('Error when run process {}: {}'.format(processor_name, e))
                        raise Exception('Error when run process {}: {}'.format(processor_name, e))

            else:
                processor_name = processor.__class__.__name__
                self.logger.info('Run processor: {}'.format(processor_name))

                try:
                    if processor_name == 'JoinProcessor':
                        processor.messages.append(_message)

                        # get chunk batch_size
                        if len(processor.messages) >= processor.batch_size:
                            _message = method(processor.messages)
                            processor.messages = []
                        else:
                            _message = None

                    elif processor_name == 'SplitProcessor':
                        _list_messages = copy.deepcopy(_message)

                        for msg in _list_messages:
                            _message = self.process(msg, chain_methods=self.methods[i + 1:])

                        return _message
                    else:
                        _message = method(_message)

                except Exception as e:
                    self.logger.error('Error when run process {}: {}'.format(processor_name, e))
                    raise Exception('Error when run process {}: {}'.format(processor_name, e))