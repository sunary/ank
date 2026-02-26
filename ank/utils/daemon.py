__author__ = 'sunary'


import os
import sys


def daemonize():
    """
    Double-fork to run as a daemon process.
    Detaches from controlling terminal and runs in background.
    """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('fork #1 failed: {}\n'.format(e))
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('fork #2 failed: {}\n'.format(e))
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    with open(os.devnull, 'r') as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    with open(os.devnull, 'a+') as devnull:
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())
