# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'flask_sqlalchemy',
    'sqlalchemy',
]

setup(
    name='qin_brick',
    version='0.0.1',
    description="qin_brick, Qin bricks. db models for flask's application",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True
)
