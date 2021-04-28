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
# ========================================================
"""KoNLP Korean morpheme analyzer Package

TODO : We will introduce the Korean morphem analyzer's feature and representative engine.
       We have to select standard Korean morpheme ananlyzer
"""

# for user, from konlp.kma import KltKma
# k = KltKma()
# from konlp.kma.klt import KltKma






## third-party Korean morpheme analyzer 

# for user, from konlp.kma impor Kkma
# k = Kkma()
from konlp.kma.kkma import Kkma


from konlp.kma.klt2000 import klt2000
