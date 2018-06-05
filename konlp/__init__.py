# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit:
#
#
# Author: HyunYoung Lee <hyun02.engineer@gmail.com>
#         GyuHyeon Nam <ngh3053@gmail.com>
#         Younghun Cho <cyh905@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ============================================================
"""KoNLP : Korean Natural Language Toolkit(KoNLTK) project

The Korean Natural Language Toolkit(KoNLTK) project is an open source Python library
for Korean Natural Langugae Processing.

Later on We would create free online book to be available.
(Then, if you use the library for academic research, Pleas cite the book.)
"""

import os

# ===========================================================
# Metadata
# ===========================================================

# Version, Fore each new release, the version number should be updated
# in the file, VERSION under konlp directory.
try:
    # If a VERSION files exists, use it!
    VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION")
    with open(VERSION_FILE, "r") as vfh:
        __version__ = vfh.read().strip()
except NameError:
    __version__ = "unknown"
except IOError as ex:
    __version__ = "unknow (%s)" % ex

# Copyright notice
__copyright__ = """\
Copyright (c) 2017 - 0000 KoNLTK Project.


which is included by reference.
"""

__license__ = ""

# Description of the toolkit, keywords, and the project's main URL
# This information is from setup.py
# IF you change the setup.py, check if this is correct with the content of setup.py
__shortdescr__ = "Korean Natural Language Toolkit"

__url__ = "https://www.konltk.org"
__longdescr__ = """\
KoNLP is Natural Language Processing Toolkit and Python package for
Korean natural Language precessing. KoNLP currently requires Python 3.5."""
__keywords__ = ['NLP', 'KoNLTK', 'NLPK',
                'koNLP', 'konltk', 'nlpk', 'konlp',
                'korean natural langugae processing', 'natural language processing',
                'parsing', 'tagging', 'tokenizing',
                'morpheme anaylisis', 'chunk',
                'natural language', 'text anayltics']

# Maintainer, contributer, etc.
__author__ = "Hyunyoung Lee" # Later on, maintainer
__author_email__ = "hyun02.engineer@gmail.com"

# "Trove" classifiers for Python Package Index
__classifiers__ = [
    # How mature is this project? common value are
    #    3 - Alpha
    #    4 - Beta
    #    5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is inteded for
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    #'License :: ',
    #'Operating System :: OS Dependent', # Later on, we change it into OS Independent
    #'Programming Language :: Python :: 2.7', # Later on, we support it
    'Programming Language :: Python :: 3.5',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Filters',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Indexing',
    'Topic :: Text Processing :: Linguistic',
]



# ===========================================================
# Package
# ===========================================================

# Later on, we have to add some package this here



# ===========================================================
# Jnius initialize
# ===========================================================

import jnius_config

jar_list = list()
cur_dir = os.path.dirname(__file__)

for (file_path, _, file_list) in os.walk(cur_dir):
    for file in file_list:
        _, file_ext = os.path.splitext(file)
        if file_ext == '.jar':
            jar_list.append(os.path.join(file_path, file))

jnius_config.add_classpath(os.pathsep.join(jar_list))