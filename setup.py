#!/usr/bin/env python

from setuptools import setup

setup(name='pySWEETCat',
      version='1.0.1',
      description='A pure-Python package to download data from SWEET-Cat',
      long_description=open('README.rst').read(),
      author='João Faria',
      author_email='joao.faria@astro.up.pt',
      license='MIT',
      url='https://github.com/j-faria/pySWEETCat',
      packages=['pysweetcat'],
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ),
     )