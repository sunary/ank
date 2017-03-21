__author__ = 'sunary'


import sys
import os
from argparse import ArgumentParser
from deploy import generate_processor, generate_setting, dependency_injection
from ank import VERSION, API_DEFAULT_PORT
from utilities import my_cmd


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
        return '''
from ank.apps.app import BaseApp


class {0}(BaseApp):

    def __init__(self, agrs, **kwagrs):
        super({0}, self).__init__()

    def run(self, process=None):
        super({0}, self).run(process)

    def process(message=None):
        return message

        '''.format(prj_name)

    elif baseapp == 'APIApp':
        endpoint_content = '''
from ank.apps.api_app import APIApp
from ank.utilities import my_api


class {0}Endpoint(APIApp):

    def __init__(self, host='localhost', port={1}):
        super({0}Endpoint, self).__init__(host, port)

    def hello(self, params):
        # host:port/hello?name=YourInput
        your_input = params.get('name')
        return my_api.success(message='Hello: %s' % (your_input))

        '''.format(prj_name, API_DEFAULT_PORT)

        with open('{}/endpoint.py'.format(prj_name), 'w') as create_file:
            create_file.write(endpoint_content)

        return '''
from endpoint import {0}Endpoint
from ank.apps.app import BaseApp


class {0}(BaseApp):

    def __init__(self, agrs, **kwagrs):
        super({0}, self).__init__()

    def run(self, process=None):
        api_app = {0}Endpoint(host='localhost', port={1})
        api_app.run()
        '''.format(prj_name, API_DEFAULT_PORT)

    elif baseapp == 'ScheduleApp':
        return '''
from ank.apps.schedule_app import ScheduleApp
from datetime import datetime


class {0}(ScheduleApp):

    def __init__(self, crontab_time, start_now=False, **kwargs):
        super({0}, self).__init__(crontab_time, start_now)

    def run(self, process=None):
        super(ScheduleApp, self).run(process)

    def process(self, message=None):
        print('Now is %s' % (datetime.now()))
        '''.format(prj_name)

    else:
        raise Exception('{} not found'.format(baseapp))


def unittest_template(prj_name):
    return '''
import os
import unittest
from ank.deploy import dependency_injection
from processor import {0}


class TestService(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, False)

    def test_function(self):
        service = {0}()

        message = None # Need initialize variable
        expected_result = None # Need initialize variable

        output_service = service.process(message)

        self.assertEqual(output_service, expected_result)

    def test_chain_processor(self):
        if os.path.exists('_processor.py'):
            import _processor
        else:
            print('generate _processor.py before run this test')

    def test_chain(self):
        dependency_injection.main('settings.yml') # replace your test setting file


if __name__ == '__main__':
    unittest.main()

    '''.format(prj_name)


def docker_template(prj_name):
    return '''
FROM alpine:3.3
MAINTAINER Developer "name@company.com"

#addition apk for image
RUN apk --update add py-pip libffi-dev openssl-dev
RUN apk --update add gettext gcc libpq python-dev git && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip

RUN mkdir -p /srv/logs
RUN mkdir -p /srv/{0}
ADD . /srv/{0}
WORKDIR /srv/{0}
RUN pip install -r requirements.txt

ENTRYPOINT []
CMD []
    '''.format(prj_name)


def services_template(prj_name, baseapp):
    if baseapp == 'BaseApp':
        return '''
services:
  {0}:
    class: processor.{0}
    arguments: ~


chains:
  - {0}
    '''.format(prj_name)

    elif baseapp == 'APIApp':
        return '''
services:
  {0}:
    class: processor.{0}
    arguments: ['%host%', '%port%']


chains:
  - {0}
        '''.format(prj_name)

    elif baseapp == 'ScheduleApp':
        return '''
services:
  {0}:
    class: processor.{0}
    arguments: ['%crontab_time%', '%start_now%']


chains:
  - {0}
        '''.format(prj_name)

    else:
        raise Exception('{} not found'.format(baseapp))


def settings_template(baseapp):
    if baseapp == 'BaseApp':
        return ''

    elif baseapp == 'APIApp':
        return '''
parameters:
  host: localhost
  port: {0}
        '''.format(API_DEFAULT_PORT)

    elif baseapp == 'ScheduleApp':
        return '''
parameters:
  crontab_time: '0 0 * * 5'
  start_now: True
        '''

    else:
        raise Exception('{} not found'.format(baseapp))


def readme_template(prj_name):
    return '''
## {0}:
Service descriptions


# generator:
- generate template settings.yml: `ank -s`
- generate _processor.py: `ank -p`

# deploy:
- build: `ank -b`
- test: `ank -t -f test-settings.yml`
- run: `ank -r`
    '''.format(prj_name)


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
    print my_cmd.run_cmd(['docker', 'build', '.'])['message']


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