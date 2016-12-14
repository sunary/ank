__author__ = 'sunary'


from utils import my_cmd


class Environment(object):
    '''
    Create virtualenv then install requirements
    '''

    def __init__(self, project):
        self.project = project

    def create(self, virtual_env='worker'):
        with my_cmd.chdir(self.project):
            my_cmd.run_cmds([
                'pwd',
                'rm -rf {}'.format(virtual_env),
                'virtualenv {}'.format(virtual_env),
                'source {}/bin/activate'.format(virtual_env),
                'pip install --no-index --find-links=lib -r requirements.txt',
                'deactivate'
            ])

    def remove(self, virtual_env='worker'):
        with my_cmd.chdir(self.project):
            my_cmd.run_cmd('rm -fr {}'.format(virtual_env))


if __name__ == '__main__':
    env = Environment('project')
    print(env.create('worker'))
    print(env.remove('worker'))