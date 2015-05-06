#!/usr/bin/env python
# coding: utf-8
"""
Python Billomat API Client Library - Setup
 
Created
    2014-10-26 by Gerold - http://halvar.at/
"""

import os
from setuptools import setup, find_packages

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "https://github.com/gerold-penz/python-billomat"
DOWNLOAD_BASEURL = "https://github.com/gerold-penz/python-billomat/raw/master/dist/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "python-billomat-%s.tar.gz" % VERSION


setup(
    name = "python-billomat",
    version = VERSION,
    description = (
        "Python Billomat API Client Library"
    ),
    long_description = open("README.rst").read(),
    keywords = (
        "Billomat, Client, API, Data Interchange, Google App Engine, REST Api"
    ),
    author = "Gerold Penz",
    author_email = "gerold@halvar.at",
    url = HOMEPAGE,
    download_url = DOWNLOAD_URL,
    packages = find_packages(),
    classifiers = [
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    install_requires = ["bunch", "urllib3"],
)

