__author__ = 'sunary'


import os
from builder.environment import Environment
from builder.git import Git


class BuildProject():
    '''
    Clone project from source, and setup environment
    '''
    def __init__(self):
        pass

    def handle(self, params):
        git = Git()
        git.handle(params)

        env = Environment(os.path.join(params.get('dest', params['dir']), params['name']))
        env.create()


if __name__ == '__main__':
    build = BuildProject()
    params = {'name': 'data-science',
              'source': 'git@github.com:sunary/data-science.git',
              'dir': ''}
    build.handle(params)