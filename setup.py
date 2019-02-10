#!/usr/bin/env python
"""
soccer_predictions:
    A package to compare different sports predictions and to predict end of season results for the current season.
"""
from typing import List
from setuptools import find_packages, setup

from __version__ import __version__

dep: List[str] = [
    'PyYAML==3.11', 'matplotlib==2.2.3', 'prettytable==0.7.2', 'requests>=2.18.3', 'wheel==0.29.0', 'ftfy==4.4.2',
    'urllib3>=1.22', 'tabulate==0.7.7', 'argparse>=1.4.0', 'h5py>=2.7.0', 'plotly>=2.0.14',
    'django-enumchoicefield==0.9.0', 'djangorestframework==3.3.3', 'Django==1.9.6', 'bs4==0.0.1', 'flake8==3.5.0',
    'PyGithub==1.38', 'XlsxWriter==1.0.5', 'termcolor', 'cvxpy==1.0.11', 'joblib==0.12.5', 'xgboost==0.81'
]


def get_dependency_links() -> list:
    links = []
    return links


setup(
    name='soccer_predictions',
    version=__version__,
    description='A sports prediction package',
    long_description='A package to research and predict end of season results for the current season.',
    url='http://github.com/gauravchak/soccer_predictions',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages(),
    install_requires=dep,
    zip_safe=False,
    include_package_data=True,
    dependency_links=get_dependency_links())
