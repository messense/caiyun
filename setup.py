#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # NOQA


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


readme = 'README.md'
if os.path.exists('README.rst'):
    readme = 'README.rst'
with open(readme) as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]


setup(
    name='caiyun',
    version='0.1.3',
    author='Messense Lv',
    author_email='messense@icloud.com',
    url='https://github.com/messense/caiyun',
    packages=find_packages(exclude=['tests']),
    keywords='zimuzu,baidu',
    description='Zimuzu resources to Baidu Yun Pan',
    long_description=long_description,
    install_requires=requirements,
    include_package_data=True,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'caiyun = caiyun.cli:main',
        ],
    },
)
