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
from konlp.kma.klt import klt

@pytest.fixture
def input_list():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

def test_morphs(input_list):
    k = klt.Klt()
    assert k.morphs(input_list)

def test_nouns(input_list):
    k = klt.Klt()
    assert k.nouns(input_list)

def test_analyze(input_list):
    k = klt.Klt()
    assert k.analyze(input_list)

def test_noun_comp(input_list):
    k = klt.Klt()
    assert k.noun_comp(input_list)