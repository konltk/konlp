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
from konlp.kma.klt2000 import klt2000

@pytest.fixture
def input_string():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def klt_instance():
    k = klt2000()
    return k

def test_morphs(klt_instance, input_string):
    assert klt_instance.morphs(input_string) == ['안녕', '국민대학교', '자연어처리', '연구실']

def test_nouns(klt_instance, input_string):
    assert klt_instance.nouns(input_string) == ['안녕', '국민대학교', '자연어처리', '연구실']

def test_pos(klt_instance, input_string):
    assert klt_instance.pos(input_string) == ['안녕/N', '국민대학교/C', '자연어처리/C', '연구실/N']
