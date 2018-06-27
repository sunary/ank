__author__ = 'sunary'


import os
from setuptools import setup, find_packages
from ank import VERSION


def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


with open('README.md') as fo:
    readme = fo.read()

with open('LICENSE') as fo:
    license = fo.read()

with open('CHANGES.md') as fo:
        changes = fo.read()

reqs = ['pyyaml==3.12',
        'flask==1.0.2',
        'redis==2.10.5',
        'pika==0.10.0',
        'pyzmq==16.0.2',
        'kafka-python==0.9.5']

setup(
    name='ank',
    version=VERSION,
    author='Sunary [Nhat Vo Van]',
    author_email='v2nhat@gmail.com',
    maintainer='Sunary [Nhat Vo Van]',
    maintainer_email='v2nhat@gmail.com',
    platforms='any',
    description='Python Streaming system, REST-API and Schedule task using queue message',
    long_description='Python Streaming system, REST-API and Schedule task using queue message\n',
    license=license,
    keywords='ank, streaming, microservice, pipeline, schedule task',
    url='https://github.com/sunary/ank',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    package_data={'templates': ['*.tpy']},
    install_requires=reqs,
    entry_points={
        'console_scripts': ['ank = ank.cli:main']
    },
)