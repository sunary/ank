__author__ = 'sunary'


import sys
import os
import argparse
import pprint
import generate_processor, generate_setting, head_process
from ank import VERSION, API_DEFAULT_PORT
from ank.utils import cmd_helpers


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


def create_setting(file_setting):
    generate_setting.main(file_setting)


def create_processor(file_setting):
    generate_processor.main(file_setting)


def test_service():
    print(cmd_helpers.run_cmd(['python', '-m', 'unittest', 'test_service'])['message'])


def run_service(file_setting):
    head_process.main(file_setting=file_setting)


def build_service():
    print(cmd_helpers.run_cmd(['docker', 'build', '.'])['message'])


def parse_args(args):
    parser = argparse.ArgumentParser(prog='Ank Streaming system')
    subparsers = parser.add_subparsers(dest='subparser')

    create_parser = subparsers.add_parser('create',
                                          help='Create new service')
    create_parser.add_argument('-c', '--class', help='App class: [default=`BaseApp`, `APIApp`, `ScheduleApp`]')

    gen_setting_parser = subparsers.add_parser('gen_setting', help='Generate `setting.yml` file')
    gen_setting_parser.add_argument('-fs', '--file_setting', help='Setting file, default `_setting.yml`')

    gen_processor_parser = subparsers.add_parser('gen_processor', help='Generate `_processor.py` file')
    gen_processor_parser.add_argument('-fs', '--file_setting', help='Setting file, default `setting.yml`')

    test_parser = subparsers.add_parser('test', help='Test service')

    run_parser = subparsers.add_parser('run', help='Run service')
    run_parser.add_argument('-fs', '--file_setting', help='Setting file, default `setting.yml`')

    build_parser = subparsers.add_parser('build', help='Build service')

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    pprint.pprint(args)
    if args.subparser_name == 'create':
        if args.c and args.c in ['BaseApp', 'APIApp', 'ScheduleApp']:
            baseapp = args.app
        else:
            baseapp = 'BaseApp'

        create(args.create, baseapp)
    elif args.subparser_name == 'gen_setting':
        create_setting(args.fs or '_settings.yml')
    elif args.subparser_name == 'gen_processor':
        create_processor(args.fs or 'setting.yml')
    elif args.subparser_name == 'test':
        test_service()
    elif args.subparser_name == 'run':
        run_service(args.fs or 'setting.yml')
    elif args.subparser_name == 'build':
        build_service()
