# setup.py
from setuptools import setup

setup(
    name='bissue',
    version='3.0',
    py_modules = ['bissue'],
    author = "Yoshimaru Shirakawa",
    license='MIT',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bie=bissue:cli
    '''
)