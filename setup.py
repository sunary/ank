__author__ = 'sunary'


import os
from setuptools import setup, find_packages
from ank import VERSION


def __path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

with open('LICENSE') as fo:
    license = fo.read()

reqs = ['pyyaml==3.12']

setup(
    name='ank',
    version=VERSION,
    author='Sunary [Nhat Vo Van]',
    author_email='v2nhat@gmail.com',
    maintainer='Sunary [Nhat Vo Van]',
    maintainer_email='v2nhat@gmail.com',
    description='Python Streaming System',
    long_description='ank - Python Streaming System, distribute tasks and more.' +
                     '<br>See at: https://github.com/sunary/ank',
    license=license,
    keywords='ank, streaming, microservice, pipeline',
    url='https://github.com/sunary/ank',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    package_data={'templates': ['*.tpy']},
    install_requires=reqs,
    entry_points={
        'console_scripts': ['ank = ank.cli:main']
    },
)