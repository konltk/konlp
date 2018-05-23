# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - kkma
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Hyunyoung Lee <Hyun02.engineer@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================

import pytest
from konlp.kma import Eunjeon

@pytest.fixture
def input_string():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def eunjeon_instance():
    ej = Eunjeon()
    return ej

def test_tokens(eunjeon_instance, input_string):
    assert eunjeon_instance.tokens(input_string) == ['안녕', '하', '세요', '.', '국민대', '학교', '자연어', '처리',
                                                     '연구실', '입니다', '.']

def test_nouns(eunjeon_instance, input_string):
    assert eunjeon_instance.nouns(input_string) == ['안녕', '국민대', '학교', '자연어', '처리', '연구실']

def test_analyze(eunjeon_instance, input_string):
    assert eunjeon_instance.analyze(input_string) == [('안녕', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF'), ('.', 'SF'),
                                                      ('국민대', 'NNP'), ('학교', 'NNG'), ('자연어', 'NNG'),
                                                      ('처리', 'NNG'), ('연구실', 'NNG'), ('입니다', 'VCP+EF'),
                                                      ('.', 'SF')]
