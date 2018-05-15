from setuptools import setup, find_packages
from os.path import join, dirname

import starring

setup(
    name='starring',
    version=starring.__version__,
    install_requires=[
        'requests==2.18.4'
    ],
    packeges=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_point={'console_scripts': ['starring = starring.__main__:main']},

)