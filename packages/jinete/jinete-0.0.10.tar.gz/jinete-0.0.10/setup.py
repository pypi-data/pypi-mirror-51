#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from distutils.util import convert_path
import itertools as it

module_name = 'jinete'

with open('README.md') as f:
    long_description = f.read()

with open(convert_path('{}/_version.py'.format(module_name))) as file:
    main_ns = dict()
    exec(file.read(), main_ns)
    module_version = main_ns['__version__']

description = (
    "High Performance solving suite for the Pickup and Delivery "
    "Problem and its related extensions."
)

dependencies = [

]

extra_dependencies = {
    'docs': [
        'sphinx',
        'sphinx-rtd-theme',
        'sphinxcontrib-apidoc',
    ],
    'tests': [
        'coverage',
        'codecov',
    ],
    'logs': [
        'coloredlogs',
    ]
}
extra_dependencies['all'] = list(it.chain(extra_dependencies.values()))

setup(
    name=module_name,
    version=module_version,
    url='https://github.com/garciparedes/jinete',
    author='Sergio García Prado',
    author_email='sergio@garciparedes.me',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description=description,
    packages=find_packages(),
    install_requires=dependencies,
    extras_require=extra_dependencies,
)
