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
from konlp.kma import Jklt

@pytest.fixture
def input_string():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def klt_instance():
    k = Jklt()
    return k

def test_tokens(klt_instance, input_string):
    assert klt_instance.tokens(input_string) == ['안녕', '세요', '국민대학교', '자연어처리', '연구실', 'B니다']

def test_nouns(klt_instance, input_string):
    assert klt_instance.nouns(input_string) == ['안녕', '국민대학교', '자연어처리', '연구실']

def test_analyze(klt_instance, input_string):
    assert klt_instance.analyze(input_string) == [['안녕', 'N'], ['세요', 'E'], ['국민대학교', 'N'], ['자연어처리', 'N'], ['연구실', 'N'], ['B니다', 'E']]
