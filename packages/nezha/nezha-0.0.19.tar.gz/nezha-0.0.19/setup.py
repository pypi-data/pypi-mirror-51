# !/usr/bin/env python
# coding: utf-8

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'pycryptodome',
    'requests',
]

setup(
    name='nezha',
    version='0.0.19',
    author='kougazhang',
    author_email='kougazhang@gmail.com',
    url='https://github.com/kougazhang',
    description="nezha, pysuway's utils",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True
)
