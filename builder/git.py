__author__ = 'sunary'


from utils import my_cmd


class Git(object):
    '''
    Clone project from git
    '''

    def __init__(self):
        pass

    def handle(self, params):
        source_code = params.get('source')
        branch = params.get('branch', 'master')
        working_dir = params.get('dir', '.')

        with my_cmd.chdir(working_dir):
            my_cmd.run_cmds([
                'pwd',
                'rm -fr %s' % (params['name']),
                'git clone %s' % (source_code),
                'git checkout %s' % (branch)
            ])