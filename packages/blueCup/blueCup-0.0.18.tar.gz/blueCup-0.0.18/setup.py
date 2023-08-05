# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'celery',
    'jsonschema',
    'nezha',
    'muzha',
    'pandas',
    'pymongo',
    'redis',
    'flower',
    'blinker',
    'gevent',
    'openpyxl',
    'ipython'
]

setup(
    name='blueCup',
    version='0.0.18',
    author='kougazhang',
    author_email='kougazhang@gmail.com',
    url='https://github.com/kougazhang',
    description="Little blue cup, who do not love?",
    packages=find_packages(),
    install_requires=install_requires,
)
