#!/usr/bin/env python3

from setuptools import setup, find_packages
import sys

version='0.0.1'

setup(
    zip_safe=True,
    name='RPi.motion',
    version=version,
    long_description="Application for detecting motion and taking some action, using a Raspberry Pi",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Programming Language :: Python :: 3",
    ],
    keywords='telegram rpi raspberry-pi',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/jdcasey/rpi.motion',
    license='GPLv3+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      "RPi.GPIO",
      "python-telegram-bot",
      "ruamel.yaml",
      "click",
      "requests",
      "datetime"
    ],
    test_suite="tests",
    entry_points={
      'console_scripts': [
        'rpi-motion-bot = rpi_motion:bot',
        'rpi-motion-send = rpi_motion:send'
      ],
    }
)

