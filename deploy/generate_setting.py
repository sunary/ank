__author__ = 'sunary'


import yaml
from utils import my_deploy, my_helper


class GenerateSetting():
    '''
    Generate settings.yml template
    '''

    def __init__(self):
        self.logger = my_helper.init_logger(self.__class__.__name__)

        self.setting_parameters = {}

    def process(self):
        self.service_loader = my_deploy.loader('services', 'services')
        chain_loader = my_deploy.loader('services', 'chains')
        for process_name in chain_loader:
            self.from_class(process_name)

        # read old settings
        try:
            setting_loader = my_deploy.loader('settings', 'parameters')
        except Exception as e:
            setting_loader = {}
            self.logger.error(e)

        for key, value in setting_loader.iteritems():
            if self.setting_parameters.get(key, '') is None:
                self.setting_parameters[key] = value

        output = yaml.dump({'parameters': self.setting_parameters}, default_flow_style=False)
        with open('_settings.yml', 'w') as of:
            of.write(output)

        return output

    def from_object(self, argument):
        argument = my_deploy.normalize_service_argument(argument)
        if argument[-1] == 'dict':
            for key, value in argument[0].iteritems():
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


def main():
    generate_setting = GenerateSetting()
    print generate_setting.process()


if __name__ == '__main__':
    main()