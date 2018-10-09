__author__ = 'sunary'


import os
import sys
sys.path.append(os.getcwd())

import importlib
from ank.core.daemon import Daemon
from ank.core.dependency_processor import DependencyProcessor
from ank.chain_process import ChainProcess
from ank.utils import naming_services, logger, config_handle


class WorkerLoader(object):

    def __init__(self):
        self.logger = logger.init_logger(self.__class__.__name__)
        self.service_loader = {}
        self.setting_loader = {}

    def start(self, file_setting='settings.yml'):
        self.service_loader = config_handle.load('services.yml', 'services')
        self.setting_loader = config_handle.load(file_setting, 'parameters')

        chain_processor = ChainProcess()
        chain_loader = config_handle.load('services.yml', 'chains')

        for process_name in chain_loader:
            self.logger.info('processor: {}'.format(process_name))

            processor = self.get_class(process_name)
            chain_processor.add_processor(DependencyProcessor(processor))

        chain_processor.methods[0][0].run(chain_processor.process)

    def get_object(self, argument):
        """
        Args:
            argument: list: [..., data_type]
        """
        argument = naming_services.normalize_service_argument(argument)

        if argument[-1] == 'dict':
            dict_argument = {}
            for key, value in argument[0].items():
                if value[-1] == 'object':
                    dict_argument[key] = self.get_class(value[0])
                elif value[-1] == 'variable':
                    dict_argument[key] = self.setting_loader[value[0]]

            return dict_argument
        elif argument[-1] == 'object':
            return self.get_class(argument[0])
        elif argument[-1] == 'variable':
            return self.setting_loader[argument[0]]

        return None

    def get_class(self, str_class):
        object_name = self.service_loader[str_class]['class']

        object_arguments = self.service_loader[str_class]['arguments']
        object_arguments = object_arguments if (type(object_arguments) is list) else [object_arguments]

        object_parameters = tuple([self.get_object(x) for x in object_arguments])

        processor = self.load_class(object_name, object_parameters)

        return processor

    @staticmethod
    def load_class(class_full_name, parameters):
        module_name, class_name = naming_services.class_name_extract(class_full_name)
        module = importlib.import_module(module_name)

        _class = getattr(module, class_name)

        if parameters[0] is None:
            return _class()

        return _class(*parameters)


def main(file_setting='settings.yml'):
    daemon = Daemon('daemon.pid')
    daemon.start()
    print(os.getpid())
    loader = WorkerLoader()
    print(loader.start(file_setting))


if __name__ == '__main__':
    main()
