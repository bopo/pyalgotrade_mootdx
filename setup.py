#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from pyalgotrade_mootdx import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pyalgotrade', 'mootdx']
test_requirements = ['pyalgotrade', 'mootdx', 'pytest',]
setup_requirements = ['pyalgotrade', 'mootdx']

setup(
    name='pyalgotrade_mootdx',
    version=__version__,
    description="pyalgotrade mootdx module",
    long_description=readme + '\n\n',
    author="bopo.wang",
    author_email='ibopo@126.com',
    url='https://github.com/bopo/pyalgotrade_mootdx',
    packages=find_packages(include=['pyalgotrade_mootdx','pyalgotrade_mootdx.*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pyalgotrade_mootdx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
