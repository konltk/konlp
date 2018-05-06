# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - klt
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#         HyunYoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
# from konlp.kma import klt

# Later on we have to remove this. 
# For klt.py
from konlp.kma.klt.lib import kma 
# we change the way to import index with cython 
from konlp.kma.klt.lib import index
