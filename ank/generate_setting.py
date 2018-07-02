__author__ = 'sunary'


from ank.utils import naming_services, config_handle, logger


class GenerateSetting(object):
    """
    Generate settings.yml template
    """

    def __init__(self):
        self.logger = logger.init_logger(self.__class__.__name__)

        self.setting_parameters = {}

    def process(self, file_setting='_settings.yml'):
        try:
            self.service_loader = config_handle.load('services.yml', 'services')
        except IOError:
            self.logger.error('IOError: file \'services.yml\' not found')
            raise IOError('file \'services.yml\' not found')
        except KeyError:
            self.logger.error('KeyError: \'services\'')
            raise KeyError('services')

        try:
            chain_loader = config_handle.load('services.yml', 'chains')
        except KeyError:
            self.logger.error('KeyError: \'chains\'')
            raise KeyError('chains')

        for process_name in chain_loader:
            if isinstance(process_name, list):
                for proc in process_name:
                    self.from_class(proc)
            else:
                self.from_class(process_name)

        # read old settings
        try:
            setting_loader = config_handle.load('settings.yml', 'parameters')
        except IOError:
            self.logger.error('IOError: file \'settings.yml\' not found')
            raise IOError('settings.yml not found')
        except KeyError:
            self.logger.error('KeyError: \'parameters\'')
            raise KeyError('parameters')

        for key, value in setting_loader.items():
            if self.setting_parameters.get(key, '') is None:
                self.setting_parameters[key] = value

        output = config_handle.save(file_setting, 'parameters', self.setting_parameters)

        return output

    def from_object(self, argument):
        argument = naming_services.normalize_service_argument(argument)
        if argument[-1] == 'dict':
            for key, value in argument[0].items():
                if value[-1] == 'object':
                    self.from_class(value[0])
                elif value[-1] == 'variable':
                    self.setting_parameters[value[0]] = None

        elif argument[-1] == 'object':
            self.from_class(argument[0])
        elif argument[-1] == 'variable':
            self.setting_parameters[argument[0]] = None

    def from_class(self, str_class):
        object_arguments = self.service_loader[str_class]['arguments']
        object_arguments = object_arguments if type(object_arguments) is list else [object_arguments]
        [self.from_object(x) for x in object_arguments]


def main(file_setting='_settings.yml'):
    generate_setting = GenerateSetting()
    print(generate_setting.process(file_setting))


if __name__ == '__main__':
    main(file_setting='_settings.yml')
