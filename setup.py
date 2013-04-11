#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'data reduction is my project for MATH 5466',
    'author': 'Will Frey',
    'url': 'none',
    'download_url': 'none',
    'author_email': 'jfrey89@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'numpy'],
    'packages': ['data-reduction'],
    'scripts': [],
    'name': 'python-data_reduction'
}

setup(**config)
