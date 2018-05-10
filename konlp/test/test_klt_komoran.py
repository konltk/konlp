# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - komoran
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.kma.komoran import komoran

@pytest.fixture
def input_str():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def obj():
    km = komoran.Komoran()
    return km

def test_morphs(obj, input_str):
    assert obj.morphs(input_str) == ['안녕', '하', '시', '어요', '.','국민', '대학교', '자연', '어', '처리', '연구실', '이', 'ㅂ니다', '.']

def test_nouns(obj, input_str):
    assert obj.nouns(input_str) == ['안녕', '국민', '대학교', '자연', '어', '처리', '연구실']

def test_analyze(obj, input_str):
    assert obj.analyze(input_str) == [('안녕', 'NNG'), ('하', 'XSV'), ('시', 'EP'), ('어요', 'EF'), ('.', 'SF'), ('국민', 'NNG'), ('대학교', 'NNG'), ('자연', 'NNG'), ('어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('이', 'VCP'), ('ㅂ니다', 'EF'), ('.', 'SF')]