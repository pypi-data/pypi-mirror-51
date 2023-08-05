#!/usr/bin/env python

import setuptools


setuptools.setup(name='abode',
      version='0.1.0',
      description='Python Environment and Package Manager',
      author='Mat Leonard',
      author_email='leonard.mat@gmail.com',
      url='https://github.com/mcleonard/abode',
      packages=['abode'],
      scripts=['cli/abode'],
      install_requires=[
          'pyyaml',
      ]
    )