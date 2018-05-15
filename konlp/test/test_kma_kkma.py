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
from konlp.kma.kkma import kkma

simple_str = "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def obj():
    kk = kkma.Kkma()
    return kk

def test_tokens(obj, simple_str):
    assert obj.tokens(simple_str) == ['안녕', '하', '세요', '.', '국민대학교', '자연어', '처리', '연구실', '이', 'ㅂ니다', '.']

def test_nouns(obj, simple_str):
    assert obj.nouns(simple_str) == ['안녕', '국민', '국민대학교', '대학교', '자연어', '자연어처리', '처리', '연구실']

def test_analyze(obj, simple_str):
    assert obj.analyze(simple_str) == [['안녕하세요.', ['안녕/NNG', '하/XSV', '세요/EFN', './SF']], ['국민대학교 자연어처리 연구실입니다.', ['국민대학교/NNG', '자연어/NNG', '처리/NNG', '연구실/NNG', '이/VCP', 'ㅂ니다/EFN', './SF']]]
