__author__ = 'sunary'


class DependencyProcessor(object):

    def __init__(self, processor):
        self.processor = processor
        self.stored_messages = []

    def run(self):
        return getattr(self.processor, 'run')()

    def execute(self, message):
        if self.class_name() == 'JoinApp':
            self.stored_messages.append(message)
            if len(self.stored_messages) >= self.getattr('batch_size'):
                message = self.stored_messages
                self.stored_messages = []
                return message
            else:
                return None

        try:
            getattr(self.processor, 'execute')(message)
        except Exception as e:
            if hasattr(self.processor, 'on_failure'):
                getattr(self.processor, 'on_failure')(message, e)
            return None
        finally:
            if hasattr(self.processor, 'on_success'):
                getattr(self.processor, 'on_success')(message)
            return message

    def class_name(self):
        return self.processor.__class__.__name__

    def getattr(self, attr_name):
        return getattr(self.processor, attr_name)
