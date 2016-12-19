__author__ = 'sunary'


from utilities import my_deploy


class GenerateProcessor(object):
    '''
    Generate processor.py help you run directly
    '''

    def __init__(self):
        self.import_libs = ['from chains.chain_processor import ChainProcessor']
        self.implement_classes = ['chain_processor = ChainProcessor()']

    def process(self, file_setting='settings.yml'):
        self.service_loader = my_deploy.loader('services.yml', 'services')
        self.setting_loader = my_deploy.loader(file_setting, 'parameters')

        str_processor = "__author__ = 'ank_generator'\n\n"

        implement_workers = []
        chain_loader = my_deploy.loader('services.yml', 'chains')
        for process_name in chain_loader:
            implement_workers.append(self.get_class(process_name))

        for lib in self.import_libs:
            str_processor += lib + '\n'
        str_processor += '\n'

        for implement in self.implement_classes:
            str_processor += implement + '\n'

        for worker in implement_workers:
            str_processor += 'chain_processor.add_processor(%s)\n' % worker

        str_processor += '%s.run(chain_processor.process)' % implement_workers[0]

        with open('_processor.py', 'w') as of:
            of.write(str_processor)

        return str_processor

    def get_object(self, argument):
        '''
        Detect object(dict, variable, object) and return string of object
        '''
        argument = my_deploy.normalize_service_argument(argument)
        if argument[-1] == 'dict':
            dict_argument = {}
            for key, value in argument[0].iteritems():
                if value[-1] == 'object':
                    dict_argument[key] = self.get_class(value[0])
                elif value[-1] == 'variable':
                    dict_argument[key] = self.setting_loader[value[0]]

            return str(dict_argument)
        elif argument[-1] == 'object':
            return str(self.get_class(argument[0]))
        elif argument[-1] == 'variable':
            variable = self.setting_loader[argument[0]]
            if hasattr(variable, '__iter__'):
                variable = ["'" + x + "'" if type(x) is str else str(x) for x in variable]
                return str(variable)
            elif type(variable) is str:
                return "'" + variable + "'"
            else:
                return str(variable)

        return None

    def get_class(self, str_class):
        '''
        Create coding from class: _class = Class(*parameters)
        '''
        object_name = self.service_loader[str_class]['class']
        class_dir, class_name = my_deploy.class_name_extract(object_name)

        str_import = 'from {} import {}'.format(class_dir, class_name)
        if str_import not in self.import_libs:
            self.import_libs.append(str_import)

        object_arguments = self.service_loader[str_class]['arguments']
        object_arguments = object_arguments if (type(object_arguments) is list) else [object_arguments]
        object_arguments = [self.get_object(x) for x in object_arguments]
        if object_arguments[0] is None:
            object_arguments = ['']

        str_deliver = '{} = {}({})'.format(self.generate_class_name(class_name), class_name, ', '.join(object_arguments))

        if str_deliver not in self.implement_classes:
            self.implement_classes.append(str_deliver)

        return self.generate_class_name(class_name)

    def generate_class_name(self, class_name):
        return my_deploy.get_deliver_from_class(class_name)


def main(file_setting='settings.yml'):
    generate_processor = GenerateProcessor()
    print(generate_processor.process(file_setting))


if __name__ == '__main__':
    main()