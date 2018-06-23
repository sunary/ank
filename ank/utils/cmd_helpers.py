__author__ = 'sunary'


import os
import subprocess


class chdir():

    def __init__(self, path):
        self.path = path
        self.last_dir = os.getcwd()

    def __enter__(self):
        if self.path:
            os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.last_dir)


def run_cmd(cmd, **kwargs):
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return_code = process.wait()
        result = 'returned {0}'.format(return_code)
        result += ' ' + process.stdout.read()
        return {'success': True,
                'message': result}
    except Exception as e:
        return {'success': False,
                'message': 'Error when execute command: {}'.format(cmd),
                'detail': str(e)}


def run_cmds(cmds, **kwargs):
    if not cmds:
        return {'success': True}

    output = {'success': True,
              'message': []}
    for cmd in cmds:
        output_cmd = run_cmd(cmd, **kwargs)
        output['message'].append(output_cmd['message'])
        if not output_cmd['success']:
            output['success'] = False
            output['detail'] = output_cmd['detail']
            break

    output['message'] = '###############'.join(output['message'])
    return output
