__author__ = 'sunary'


import os
import unittest
from ank.program_loader import ProgramLoader
from ank.generate_processor import GenerateProcessor
from ank.generate_setting import GenerateSetting


# Tests run from ank/tests/ directory where services.yml, settings.yml, processor.py exist
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(TESTS_DIR))


class TestDeploy(unittest.TestCase):
    """
    Run from project root: python -m unittest discover -s ank/tests -p 'test_*.py'
    Or: cd ank/tests && python -m unittest test_deploy
    """

    def setUp(self):
        import sys
        self._orig_cwd = os.getcwd()
        os.chdir(TESTS_DIR)
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        if TESTS_DIR not in sys.path:
            sys.path.insert(0, TESTS_DIR)

    def tearDown(self):
        os.chdir(self._orig_cwd)

    def test_program_loader(self):
        loader = ProgramLoader()
        print('\n\n## Head Dependency Injection:')
        loader.start()

    def test_gen_processor(self):
        generate_processor = GenerateProcessor()
        print('\n\n## Generate Processor:')
        print(generate_processor.process())

    def test_gen_setting(self):
        generate_setting = GenerateSetting()
        print('\n\n## Generate Setting:')
        print(generate_setting.process())


if __name__ == '__main__':
    unittest.main()
