#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re
import os
import sys


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]",
        init_py, re.MULTILINE).group(1)


package = 'iosfu'
version = get_version(package)

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': version}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name='iosfu',
    version=version,
    url='http://github.com/fmartingr/iosfu',
    license='MIT',
    description='iOS Forensics Utility',
    author='Felipe Martin',
    author_email='fmartingr@me.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience'
        'Operating System :: OS Independent',
        'Programming Language :: Python ;; 2.7',
        'Programming Language :: Python ;; 3.3',
        'Topic :: Security',
    ]
)
