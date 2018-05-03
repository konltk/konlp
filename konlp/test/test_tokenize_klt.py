# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Klt 형태소 분석기 for Korean Natural Language Toolkit
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.tokenize import klt_asp

def test_asp():
    assert klt_asp(text="국민대학교자연어처리연구실") == ['국민대학교', '자연어처리', '연구실']
    assert klt_asp(text="국민대학교자연어처리연구실", split=False) == '국민대학교 자연어처리 연구실'
    assert klt_asp(text="국민대학교자연어처리연구실", split=True) == ['국민대학교', '자연어처리', '연구실']
