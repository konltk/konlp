# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Setup script for Korean Natural Language Toolkit
#
# Author: HyunYoung Lee <hyun02.engineer@gmail.com>
#         GyuHyeon Nam <ngh3053@gmail.com>
#         Younghun Cho <cyh905@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""Setup scirpt for Korean Natural Language Tooklit"""

import os
from setuptools import setup, find_packages

# Use the VERSION FILE under konlp directory to get konlp version
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'konlp', 'VERSION')
with open(VERSION_FILE) as vfh:
    KONLP_VERSION = vfh.read().strip()

# Setuptools
setup(
    name="konlp",
    description="Korean Natural Language Toolkit",
    version=KONLP_VERSION, # We are dealing with as variable by reading VERSION file under konlp directory 
    url="https://www.konltk.org",
    long_description="""\
KoNLP is Natural Language Processing Toolkit and Python package for
Korean natural Language precessing. KoNLP currently requires Python 3.5.""",
    license="", # later on, We select it
    keywords=['NLP', 'KoNLTK', 'NLPK',
              'koNLP', 'konltk', 'nlpk', 'konlp',
              'korean natural langugae processing', 'natural language processing',
              'parsing', 'tagging', 'tokenizing',
              'morpheme anaylisis', 'chunk',
              'natural language', 'text anayltics'],
    author="Hyunyoung Lee, GyuHyeon Nam", # Later on, maintainer
    author_email="hyun02.engineer@gmail.com, ngh3053@gmail.com",
    classifiers=[
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
    ],
    package_data={'konlp':['*/*/lib/*', 'VERSION', 'test/files/*',
    # kma/klt 모듈의 사전 파일 위치
    'kma/klt/data/hdic/*',
    # kma/komoran 모듈의 사전 파일 위치
    'kma/komoran/data/models-full/*',
    'kma/komoran/data/models-light/*',
    # tokenize/klt 모듈의 사전 파일 위치
    'tokenize/klt/data/dic/*',
    ]}, # Later on we have to change it
    install_requires=[], # Later on, we have to select
    packages=find_packages(), # later on, with exclude setting
    extras_require={}, # Later on, refer to k-NLTK resource
    python_requires='>=3', # Later on, we change this to classifier above
    zip_safe=False, # Later on, we look for exact reason
    # Later on, We have to search for additional condition from Python
    )
