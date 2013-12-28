#! /usr/bin/env python

__author__ = 'bbowman@pacificbiosciences.com'

from setuptools import setup, Extension, find_packages
import sys

desc = 'Tools for analyzing large metagenomic contigs'

if ("install" in sys.argv) and sys.version_info < (2, 7, 0):
    raise SystemExit("MetagenomicsTools requires Python 2.7")

setup(
    name = 'MetagenomicTools',
    version='0.1',
    author='Brett Bowman',
    author_email='bbowman@pacificbiosciences.com',
    url='https://github.com/bnbowman/MetagenomicTools',
    description=desc,
    license=open('LICENSES.txt').read(),
    packages = find_packages('src'),
    package_dir = {'':'src'},
    zip_safe = False,
    install_requires=[
        'h5py >= 2.0.1',
        'numpy >= 1.8.0',
        'pbcore >= 0.8.0',
        ]
    )