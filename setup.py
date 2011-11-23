#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='calais',
      py_modules = ['calais'],
      description='Python interface to the OpenCalais API',
      long_description="This Python module is a wrapper around the OpenCalais API as documented at http://www.opencalais.com/calaisAPI by Reuters. It makes REST calls to the OpenCalais API via HTTP POST, then parses and simplifies the JSON responses returned by OpenCalais. You can then access the response data in a much more pythonic manner.",
      url='http://code.google.com/p/python-calais/',
      license = 'BSD License',
      keywords = "opencalais",
      classifiers = [ "License :: OSI Approved :: BSD License",
                      "Programming Language :: Python" ],
      install_requires=["simplejson>=2.0"]
)