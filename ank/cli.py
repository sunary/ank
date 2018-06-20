__author__ = 'sunary'


import sys
import os
from argparse import ArgumentParser
from deploy import generate_processor, generate_setting, dependency_injection
from ank import VERSION, API_DEFAULT_PORT
from utils import cmd_helpers


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def create(prj_name, baseapp):
    if not os.path.exists(prj_name):
        os.makedirs(prj_name)

    with open('{}/__init__.py'.format(prj_name), 'w') as create_file:
        create_file.write('')

    with open('{}/processor.py'.format(prj_name), 'w') as create_file:
        create_file.write(processor_template(prj_name, baseapp))

    with open('{}/test_service.py'.format(prj_name), 'w') as create_file:
        create_file.write(unittest_template(prj_name))

    with open('{}/requirements.txt'.format(prj_name), 'w') as create_file:
        create_file.write('ank=={}'.format(VERSION))

    with open('{}/Dockerfile'.format(prj_name), 'w') as create_file:
        create_file.write(docker_template(prj_name))

    with open('{}/services.yml'.format(prj_name), 'w') as create_file:
        create_file.write(services_template(prj_name, baseapp))

    with open('{}/settings.yml'.format(prj_name), 'w') as create_file:
        create_file.write(settings_template(baseapp))

    with open('{}/README.md'.format(prj_name), 'w') as create_file:
        create_file.write(readme_template(prj_name))


def processor_template(prj_name, baseapp):
    if baseapp == 'BaseApp':
        with open(os.path.join(CURRENT_PATH, '../templates/baseapp_processor.tpy'), 'r') as of:
            return of.read().format(prj_name)

    elif baseapp == 'APIApp':
        with open(os.path.join(CURRENT_PATH, '../templates/apiapp_endpoint.tpy'), 'r') as of:
            endpoint_content = of.read().format(prj_name, API_DEFAULT_PORT)

        with open(os.path.join(CURRENT_PATH, '{}/endpoint.py'.format(prj_name)), 'w') as create_file:
            create_file.write(endpoint_content)

        with open(os.path.join(CURRENT_PATH, '../templates/apiapp_processor.tpy'), 'r') as of:
            return of.read().format(prj_name, API_DEFAULT_PORT)

    elif baseapp == 'ScheduleApp':
        with open(os.path.join(CURRENT_PATH, '../templates/scheduleapp_processor.tpy'), 'r') as of:
            return of.read().format(prj_name)

    else:
        raise Exception('{} not found'.format(baseapp))


def unittest_template(prj_name):
    with open(os.path.join(CURRENT_PATH, '../templates/unittest.tpy'), 'r') as of:
        return of.read().format(prj_name).format(prj_name)


def docker_template(prj_name):
    with open(os.path.join(CURRENT_PATH, '../templates/docker.tpy'), 'r') as of:
        return of.read().format(prj_name).format(prj_name)


def services_template(prj_name, baseapp):
    if baseapp == 'BaseApp':
        with open(os.path.join(CURRENT_PATH, '../templates/baseapp_services.tpy'), 'r') as of:
            return of.read().format(prj_name)

    elif baseapp == 'APIApp':
        with open(os.path.join(CURRENT_PATH, '../templates/apiapp_services.tpy'), 'r') as of:
            return of.read().format(prj_name)

    elif baseapp == 'ScheduleApp':
        with open(os.path.join(CURRENT_PATH, '../templates/scheduleapp_services.tpy'), 'r') as of:
            return of.read().format(prj_name)

    else:
        raise Exception('{} not found'.format(baseapp))


def settings_template(baseapp):
    if baseapp == 'BaseApp':
        with open(os.path.join(CURRENT_PATH, '../templates/baseapp_settings.tpy'), 'r') as of:
            return of.read()

    elif baseapp == 'APIApp':
        with open(os.path.join(CURRENT_PATH, '../templates/apiapp_settings.tpy'), 'r') as of:
            return of.read().format(API_DEFAULT_PORT)

    elif baseapp == 'ScheduleApp':
        with open(os.path.join(CURRENT_PATH, '../templates/scheduleapp_settings.tpy'), 'r') as of:
            return of.read()

    else:
        raise Exception('{} not found'.format(baseapp))


def readme_template(prj_name):
    with open(os.path.join(CURRENT_PATH, '../templates/readme.tpy'), 'r') as of:
        return of.read().format(prj_name)


def create_setting():
    generate_setting.main()


def create_processor(file_setting):
    generate_processor.main(file_setting)


def test():
    # print my_cmd.run_cmd(['python', '-m', 'unittest', 'test_service'])['message']
    pass


def run():
    dependency_injection.main()


def build():
    print cmd_helpers.run_cmd(['docker', 'build', '.'])['message']


def main(options=None):
    parser = ArgumentParser(prog='Ank Microservices')

    parser.add_argument('-c', '--create', dest='create', type=str,
                        help='create new microservice with a name, should be a ClassName in code conventions')
    parser.add_argument('-a', '--app', dest='app', type=str,
                        help='app template, default is BaseApp')

    parser.add_argument('-s', '--setting', dest='setting', action='count',
                        help='generate settings.yml template')

    parser.add_argument('-p', '--processor', dest='processor', action='count',
                        help='generate _processor.py')

    parser.add_argument('-t', '--test', dest='test', action='count',
                        help='test your microservice')
    parser.add_argument('-f', '--file', dest='file_setting', type=str,
                        help='test with setting file, default is settings.yml')

    parser.add_argument('-r', '--run', dest='run', action='count',
                        help='start/restart your microservice')

    parser.add_argument('-b', '--build', dest='build', action='count',
                        help='build your microservice')

    args = parser.parse_args()

    file_setting = args.file_setting if args.file_setting else 'settings.yml'

    if args.create:
        baseapp = 'BaseApp'
        if args.app and args.app in ['BaseApp', 'APIApp', 'ScheduleApp']:
            baseapp = args.app

        create(args.create, baseapp)
    elif args.app:
        print('Using command: "ank -c NameApp -a BaseApp" to create new microservice')
    elif args.setting:
        create_setting()
    elif args.processor:
        create_processor(file_setting)
    elif args.test:
        test()
    elif args.run:
        run()
    elif args.build:
        build()
    else:
        parser.print_help()


if __name__ == '__main__':
    main(sys.argv[1:])