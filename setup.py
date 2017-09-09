__author__ = 'sunary'


import os
from setuptools import setup, find_packages
from ank import VERSION


def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

with open('LICENSE') as fo:
    license = fo.read()

reqs = ['pika==0.10.0', 'pymongo==3.4.0', 'amqp==1.4.9', 'pyyaml==3.11',
        'redis==2.10.5', 'flask==0.11', 'gevent==1.1.1']

setup(
    name='ank',
    version=VERSION,
    author='Sunary [Nhat Vo Van]',
    author_email='v2nhat@gmail.com',
    maintainer='Sunary [Nhat Vo Van]',
    maintainer_email='v2nhat@gmail.com',
    description='Python Microservices',
    long_description='ank - Microservices.<br>See at: https://github.com/sunary/ank',
    license=license,
    keywords='ank, microservice, rabbitMQ, kafka, zeroMQ, queue, streaming',
    url='https://github.com/sunary/ank',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    package_data={'templates': ['*.tpy']},
    install_requires=reqs,
    entry_points={
        'console_scripts': ['ank = ank.cli:main']
    },
)