__author__ = 'sunary'


import sys
import os
import argparse
from ank import generate_processor, generate_setting, program_loader
from ank import VERSION, API_DEFAULT_PORT
from ank.constants import BASE_APP, API_APP, SCHEDULE_APP
from ank.utils import cmd_helpers
from ank.template_loader import render_app


def create(prj_name, baseapp):
    """Create new app from templates."""
    if not os.path.exists(prj_name):
        os.makedirs(prj_name)

    files = render_app(baseapp, prj_name, API_DEFAULT_PORT, VERSION)

    for filename, content in files.items():
        path = os.path.join(prj_name, filename)
        with open(path, 'w') as f:
            f.write(content)


def create_setting(file_setting):
    generate_setting.main(file_setting)


def create_processor(file_setting):
    generate_processor.main(file_setting)


def test_service():
        print(cmd_helpers.run_cmd([sys.executable, '-m', 'unittest', 'test_service'])['message'])


def run_service(file_setting, daemon=False):
    program_loader.main(file_setting=file_setting, daemon=daemon)


def build_service():
    print(cmd_helpers.run_cmd(['docker', 'build', '.'])['message'])


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='ank',
        description='ANK - Python streaming system for pipelines, REST APIs, and message queues.',
        epilog='Examples:\n'
               '  ank create myapp -c APIApp\n'
               '  ank run -fs settings.yml\n'
               '  ank run -d',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
    subparsers = parser.add_subparsers(dest='subparser', metavar='command')

    create_parser = subparsers.add_parser(
        'create',
        help='Create a new project from templates',
        description='Scaffold a new ANK project with processor, services, and settings.',
    )
    create_parser.add_argument('name', help='Project directory name')
    create_parser.add_argument('-c', '--class', dest='app_class',
                               choices=[BASE_APP, API_APP, SCHEDULE_APP],
                               default=BASE_APP,
                               help='App type: BaseApp (pipeline), APIApp (REST API), ScheduleApp (cron) (default: %(default)s)')

    gen_setting_parser = subparsers.add_parser(
        'gen_setting',
        help='Generate settings file from services.yml',
        description='Create or update settings.yml with parameters from services.yml.',
    )
    gen_setting_parser.add_argument('-fs', '--file_setting', metavar='FILE',
                                   help='Output settings file (default: _settings.yml)')

    gen_processor_parser = subparsers.add_parser(
        'gen_processor',
        help='Generate processor module from settings',
        description='Create _processor.py with processor classes from settings.yml.',
    )
    gen_processor_parser.add_argument('-fs', '--file_setting', metavar='FILE',
                                     help='Settings file to read (default: setting.yml)')

    test_parser = subparsers.add_parser(
        'test',
        help='Run unit tests',
        description='Execute test_service.py with unittest.',
    )

    run_parser = subparsers.add_parser(
        'run',
        help='Run the service pipeline',
        description='Load services.yml and settings, then run the configured chain.',
    )
    run_parser.add_argument('-fs', '--file_setting', metavar='FILE',
                           help='Settings file (default: setting.yml)')
    run_parser.add_argument('-d', '--daemon', action='store_true',
                           help='Run in background (daemon mode)')

    build_parser = subparsers.add_parser(
        'build',
        help='Build Docker image',
        description='Run docker build in the current directory.',
    )

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    if args.subparser is None:
        parse_args(['--help'])
        return

    if args.subparser == 'create':
        create(args.name, args.app_class)
    elif args.subparser == 'gen_setting':
        create_setting(args.fs or '_settings.yml')
    elif args.subparser == 'gen_processor':
        create_processor(args.fs or 'setting.yml')
    elif args.subparser == 'test':
        test_service()
    elif args.subparser == 'run':
        run_service(args.fs or 'setting.yml', daemon=args.daemon)
    elif args.subparser == 'build':
        build_service()


if __name__ == '__main__':
    main()
