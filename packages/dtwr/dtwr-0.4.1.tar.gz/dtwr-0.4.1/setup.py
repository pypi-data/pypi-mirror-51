#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import Cython
#from numpy.distutils.misc_util import Configuration
import numpy


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


ext = [Extension('dtwr._dtw_utils',
                 sources=['dtwr/dtw_computeCM.c', 'dtwr/_dtw_utils.pyx'],
                 include_dirs=[numpy.get_include()])]


setup(
    author="Toni Giorgino",
    author_email='toni.giorgino@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="(Obsolete package: please use dtw-python). A comprehensive implementation of dynamic time warping (DTW) algorithms in R. DTW computes the optimal (least cumulative distance) alignment between points of two time series. Common DTW variants covered include local (slope) and global (window) constraints, subsequence matches, arbitrary distance definitions, normalizations, minimum variance matching, and so on. Provides cumulative distances, alignments, specialized plot styles, etc.",
    entry_points={
        'console_scripts': [
            'dtw=dtwr._cli:main',
        ],
    },
    install_requires=['numpy>=1.12', 'scipy>=1.1', 'cython>=0.29'],
#    setup_requires=['cython', 'numpy'],
#    tests_require=[],
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dtwr',
    name='dtwr',
    #    packages=find_packages(include=['dtwr']),
    packages=['dtwr'],
    package_data={'dtwr': ['data/*.csv']},
    ext_modules=cythonize(ext),
    cmdclass={'build_ext': Cython.Build.build_ext},
    test_suite='tests',
    url='https://DynamicTimeWarping.github.io',
    version='0.4.1',
    zip_safe=False,
)
