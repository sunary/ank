__author__ = 'sunary'


import yaml


def load(file_name, object_name):
    with open(file_name, 'r') as fo:
        service_loader = yaml.load(fo)
        return service_loader[object_name]


def save(file_name, key, data):
    output = yaml.dump({key: data}, default_flow_style=False)
    with open(file_name, 'w') as of:
        of.write(output)

    return output

