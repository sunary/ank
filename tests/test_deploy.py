__author__ = 'sunary'


import unittest
from deploy.dependency_injection import DependencyInjection
from deploy.generate_processor import GenerateProcessor
from deploy.generate_setting import GenerateSetting


class TestDeploy(unittest.TestCase):
    '''
    To run this test, copy services.yml, settings.yml and processor.py to root folder
    '''
    def test_di(self):
        di = DependencyInjection()
        print('\n\n## Dependency Injection:')
        di.start()

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
