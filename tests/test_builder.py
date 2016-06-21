__author__ = 'sunary'


import unittest
from builder.environment import Environment


class MyTestCase(unittest.TestCase):

    def test_git(self):
        pass

    def test_create_project(self):
        env = Environment('demo_app')
        env.create()


if __name__ == '__main__':
    unittest.main()
