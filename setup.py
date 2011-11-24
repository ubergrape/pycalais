#!/usr/bin/env python
# coding: utf-8
from distutils.core import setup

from calais import __version__ as VERSION


classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Environment :: Web Environment",
    "License :: OSI Approved :: BSD License",
    "Development Status :: 5 - Production/Stable",
]

requires = ["rdflib==3.0", "rdfextras==0.1", ]
# This might not be the best idea, but I did not encounter any bug
# while testing with both libraries.
try:
    import json
except ImportError:
    requires.append('simplejson>=2.0')


setup(name='pycalais',
      version=VERSION,
      license='BSD',
      url='https://github.com/newsgrape/pycalais',
      py_modules=['calais', 'calais_rdf'],
      description='Python interface to the OpenCalais REST API',
      long_description=open('README.rst').read(),
      keywords="opencalais calais rdf",
      classifiers=classifiers,
      install_requires=requires,
)
