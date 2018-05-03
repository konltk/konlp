# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Autospacing of klt 
#
# Author: Younghun Cho <cyh905@gmail.com>
#         HyunYoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.tokenize import KltAsp

def test_asp():
    k = KltAsp()
    assert k.asp(text="국민대학교자연어처리연구실") == ['국민대학교', '자연어처리', '연구실']
    assert k.asp(text="국민대학교자연어처리연구실", split=False) == '국민대학교 자연어처리 연구실'
    assert k.asp(text="국민대학교자연어처리연구실", split=True) == ['국민대학교', '자연어처리', '연구실']
