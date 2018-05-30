# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean automatic word spacing
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
from konlp.tokenize import KmuAsp


asp = KmuAsp()

def test_tokenize():
    assert asp.tokenize('국민대자연어처리연구실입니다.') == ['국민대 자연어처리 연구실입니다.']

def test_tokenize_sents():
    assert asp.tokenize_sents(['국민대자연어처리연구실입니다.', '나는밥을먹고학교에갔다.']) == ['국민대 자연어처리 연구실입니다.', '나는 밥을 먹고 학교에 갔다.']
