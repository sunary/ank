__author__ = 'sunary'


import yaml


def loader(file_name, object_name):
    with open('%s.yml' % file_name, 'r') as fo:
        service_loader = yaml.load(fo)
        return service_loader[object_name]


def normalize_service_argument(argument):
    '''
    normalize service name and set type: $object, $variable$
    Examples:
        >>> normalize_service_argument('$Mongodb')
        ['Mongodb', 'object']
        >>> normalize_service_argument('%batch_size%')
        ['batch_size', 'variable']
    '''
    if isinstance(argument, dict):
        dict_argument = {}

        for key, value in argument.iteritems():
            if value.startswith('$'):
                dict_argument[key] = [value[1:], 'object']
            elif value.startswith('%') and value.endswith('%'):
                dict_argument[key] = [value[1:-1], 'variable']

        return [dict_argument, 'dict']
    elif type(argument) is str:
        if argument.startswith('$'):
            return [argument[1:], 'object']
        elif argument.startswith('%') and argument.endswith('%'):
            return [argument[1:-1], 'variable']

    return [None]


def class_name_extract(class_full_name):
    '''
    extract class name to write import
    Examples:
        >>> class_name_extract('redis.client.StrictRedis')
        ('redis.client', 'StrictRedis')
    '''
    class_split = class_full_name.split('.')
    module_name = '.'.join(class_split[:-1])
    class_name = class_split[-1]

    return module_name, class_name


def get_deliver_from_class(class_name):
    '''
    Create deliver name from Class Name
    Examples:
        >>> get_deliver_from_class('DemoApp')
        '_demo_app'
    '''
    import string

    alphabeta_uppercase = string.uppercase
    splited_text = []
    last_position = 0
    for i in range(1, len(class_name)):
        if class_name[i] in alphabeta_uppercase:
            splited_text.append(class_name[last_position:i].lower())
            last_position = i

    splited_text.append(class_name[last_position:len(class_name)].lower())

    return '_' + '_'.join(splited_text)


if __name__ == '__main__':
    import doctest
    doctest.testmod()