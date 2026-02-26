__author__ = 'sunary'


import os
from setuptools import setup, find_packages
from ank import VERSION


def _path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


with open(_path('README.md')) as fo:
    readme = fo.read()

with open(_path('LICENSE')) as fo:
    license = fo.read()

reqs = ['pyyaml>=6.0',
        'flask>=3.1',
        'redis>=7.0',
        'pika>=1.3',
        'pyzmq>=26.0',
        'kafka-python>=2.2']

setup(
    name='ank',
    version=VERSION,
    python_requires='>=3.10',
    author='Sunary [Nhat Vo Van]',
    author_email='v2nhat@gmail.com',
    maintainer='Sunary [Nhat Vo Van]',
    maintainer_email='v2nhat@gmail.com',
    platforms='any',
    description='Python Streaming system, REST-API and Schedule task using queue message',
    long_description=readme,
    long_description_content_type='text/markdown',
    license=license,
    keywords='ank, streaming, microservice, pipeline, schedule task',
    url='https://github.com/sunary/ank',
    packages=find_packages(exclude=['docs', 'examples', 'tests', 'ank.tests']),
    package_data={'ank': ['templates/*.tpy']},
    install_requires=reqs,
    entry_points={
        'console_scripts': ['ank = ank.cli:main']
    },
)