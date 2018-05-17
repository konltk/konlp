# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Klt 형태소 분석기 for Korean Natural Language Toolkit
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Hyunyoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.kma.klt import klt

@pytest.fixture
def input_list():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def object():
    k = klt.KltKma()
    return k

def test_morphs(object, input_list):
    assert object.tokens(input_list) == ['안녕', '하', '세요', '.', '국민대학교', '자연어처리', '연구실', '이', '습니다', '.']

def test_nouns(object, input_list):
    assert object.nouns(input_list) == ['안녕', '국민대학교', '자연어처리', '연구실']

def test_analyze(object, input_list):
    assert object.analyze(input_list) == [('안녕하세요', [('안녕', 'N'), ('하', 't'), ('세요', 'e')]), ('.', [('.', 'q')]), ('국민대학교', [('국민대학교', 'N')]), ('자연어처리', [('자연어처리', 'N')]), ('연구실입니다', [('연구실', 'N'), ('이', 'c'), ('습니다', 'e')]), ('.', [('.', 'q')])]

def test_noun_comp(object):
    assert object.cnouns("국민대학교자연어처리연구실") == ['국민', '대학교', '자연어', '처리', '연구실']
