#!/usr/bin/python
#===============================================================================
# Copyright (C) 20122-18 Adrian Hungate
#
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#===============================================================================
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

from setuptools import setup
#from fuse_mmb import version
version = 0.6

readme = open('README.rst').read()
changes = open('CHANGES.rst').read()

setup(
    name = "PyMMBtool",
    version = str(version),
    description = "Command line tools to manage BBC Microcomputer DFS disk images and MMB disk bundles",
    author = "Adrian Hungate",
    author_email = "adrian@limbicly.com",
    url = "https://projects.limbicly.com/adrian/PyMMB",
    requires = ["PyMMB (>=0.6)"],
    scripts = [
        'dfs_cat.py',
        'dfs_compact.py',
        'dfs_create.py',
        'dfs_erase_file.py',
        'dfs_list_files.py',
        'dfs_get_file.py',
        'dfs_put_file.py',
        'mmb_cat.py',
        'mmb_compact.py',
        'mmb_create.py',
        'mmb_erase_file.py',
        'mmb_format.py',
        'mmb_list_files.py',
        'mmb_get_disc.py',
        'mmb_get_file.py',
        'mmb_put_disc.py',
        'mmb_put_file.py',
        'mmb_unformat.py',
    ],
    platforms = ['noarch'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
    long_description = readme + "\n" + changes
)
