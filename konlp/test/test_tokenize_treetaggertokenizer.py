# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean automatic TreeTagger tokenizer
#
#
# Author: SungHwan Son <zldejagkcm@naver.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
from konlp.tokenize.treetaggertokenizer.treetaggertokenizer import TreetaggerTokenizer

def test_treetaggertokenizer():
    tt = TreetaggerTokenizer()
    assert tt.tokenize(string="국민대학교 '자연어처리 연구실'입니다.") == ['국민대학교', "'", '자연어처리', '연구실', "'", '입니다', '.']
    assert tt.tokenize(string="본 소스는 'Treetagger Tokenizer'를 파이썬으로 포팅한 소스입니다.") == ['본', '소스는', "'", 'Treetagger', 'Tokenizer', "'", '를', '파이썬으로', '포팅한', '소스입니다', '.']

