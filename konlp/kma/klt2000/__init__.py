# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - kkma
#
#
# Author: Jungmin Kim <ty911007@naver.com>
#         Hyunyoung Lee <hyun02.engieer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""KoNLP Korean morpheme analyzer Package - kkma

TODO : We will introduce kkma in detail.
"""

# for user, from konlp.kma.kkma impor Kkma
# k = Kkma()
from konlp.kma.klt2000.klt2000 import klt2000

import platform
import os
import subprocess

def install():
    if not os.path.isdir(os.path.join(konlp.__path__[0],'lib_win')):
        os.mkdir(os.path.join(konlp.__path__[0],'lib_win'))
    if not os.path.isdir(os.path.join(konlp.__path__[0],'lib_win','jpype')):
        subprocess.check_call([sys.executable,"-m","pip","install","--target="+os.path.join(konlp.__path__[0], 'lib_win'),"jpype1-py3"])
#if platform.system() == 'Windows':
#    install()