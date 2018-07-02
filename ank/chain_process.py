__author__ = 'sunary'


from ank.utils import logger
import copy


CONTENT_KEY = 'content'
FLAGS_KEY = 'flags'


class ChainProcess(object):
    """
    Run chain processors
    Output of a processor will be input of the next processor
    """

    def __init__(self):
        self.logger = logger.init_logger(self.__class__.__name__)

        self.methods = []

    def run(self):
        if self.methods:
            self.methods[0][0].run(self.process())
        else:
            self.logger.error('KeyError: methods empty')
            raise KeyError('methods empty')

    def add_processor(self, processor, method='process'):
        """
        add processor(s) and method(n) into chain
        """
        if isinstance(processor, list):
            list_methods = []
            for proc in processor:
                list_methods.append(getattr(proc, method))

            self.methods.append((processor, list_methods))
        else:
            self.methods.append((processor, getattr(processor, method)))

    def process(self, message=None, chain_methods=None):
        """
        Process chain depend methods registered
        """
        _message = copy.deepcopy(message)
        chain_methods = chain_methods or self.methods

        for i, (current_processor, current_method) in enumerate(chain_methods):
            if _message is None:
                return None

            if isinstance(current_processor, (list, tuple)):
                if not _message.get(FLAGS_KEY) or not isinstance(_message[FLAGS_KEY], (list, tuple)):
                    _log_msg = 'message must to have FLAGS_KEY attribute with type is list or tuple'
                    self.logger.error('TypeError ' + _log_msg)
                    raise TypeError(_log_msg)

                temp_message = copy.deepcopy(_message)
                _message.pop(FLAGS_KEY)
                for j, status in enumerate(temp_message[FLAGS_KEY]):
                    if status:
                        processor_name = current_processor[j].__class__.__name__
                        self.logger.info('Run processor: {}'.format(processor_name))

                        try:
                            self.process(_message, chain_methods=chain_methods[i + 1:])
                        except Exception as e:
                            _log_msg = 'when run process {}'.format(processor_name)
                            self.logger.error(type(e).__name__ + ' ' + _log_msg)
                            self.logger.error(e)
                            raise type(e)(_log_msg + '\n' + str(e))

                return None

            else:
                processor_name = current_processor.__class__.__name__
                self.logger.info('Run processor: {}'.format(processor_name))

                try:
                    if processor_name == 'JoinApp':
                        current_processor.stored_messages[CONTENT_KEY].append(_message[CONTENT_KEY])

                        # get chunk batch_size
                        if len(current_processor.stored_messages[CONTENT_KEY]) >= current_processor.batch_size:
                            _message = copy.deepcopy(current_processor.stored_messages)
                            current_processor.stored_messages[CONTENT_KEY] = []
                        else:
                            return None

                    elif processor_name == 'SplitApp':
                        for msg in _message[CONTENT_KEY]:
                            self.process({CONTENT_KEY: msg}, chain_methods=chain_methods[i + 1:])

                        return None
                    else:
                        _message = current_method(_message)

                except Exception as e:
                    _log_msg = 'when run process {}'.format(processor_name)
                    self.logger.error(type(e).__name__ + ' ' + _log_msg)
                    self.logger.error(e)
                    raise type(e)(_log_msg + '\n' + str(e))
