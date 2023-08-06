#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import sys
import codecs
import os
from os.path import join, exists


name = 'ojextends'
package = 'ojextends'
description = 'A lightweight library for transferring json to nested objects.'
url = 'https://github.com/bob4open/ojextends'
author = 'Bob Wu'
author_email = 'bob4open@gmail.com'
license = 'MIT'
keywords = 'json, rest, models, object, extend'
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4'
]

install_requires = []


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(join(package, '__init__.py')).read()
    version = re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


def get_readme(package):
    with codecs.open('README.md', 'r', 'utf-8') as fd:
        return fd.read()

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not exists(join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([join(base, filename) for filename in filenames])
    return {package: filepaths}


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    args = {'version': get_version(package)}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    long_description=get_readme(package),
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=install_requires,
    classifiers=classifiers
)
