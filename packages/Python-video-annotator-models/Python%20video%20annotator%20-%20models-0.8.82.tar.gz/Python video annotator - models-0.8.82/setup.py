#!/usr/bin/python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re, os

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(PACKAGE_PATH, 'pythonvideoannotator_models','__init__.py'), 'r') as fd:
    content = fd.read()
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

setup(
	name='Python video annotator - models',
	version=version,
	description="""""",
	author=['Ricardo Ribeiro'],
	author_email='ricardojvr@gmail.com',
	url='https://bitbucket.org/fchampalimaud/pythonvideoannotator-models',
	packages=find_packages(),	
)
