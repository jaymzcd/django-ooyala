#!/usr/bin/env python

from setuptools import setup

setup(name='django-ooyala',
      version='0.9.3',
      description='A django library for interacting with the Ooyala video platform',
      author='Jaymz Campbell',
      author_email='jaymz@jaymz.eu',
      url='https://github.com/jaymzcd/django-ooyala',
      packages=['ooyala', 'ooyala.templatetags', 'ooyala.templates', 'ooyala.management'],
     )
