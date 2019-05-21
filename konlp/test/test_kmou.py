# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: pyTest
#
# Author: Jae-Hoon Kim <jhoon@kmou.ac.kr>
#         Ho Yoon <4168615@naver.com>
#         Young Namgoong <aei0109@naver.com>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.tokenize import SentenceTokenizer
from konlp.tokenize import WordSegment
from konlp.tag import VXP_ChunkTagger
from konlp.tag import JSP_ChunkTagger
from konlp.tag import NERTagger
import konlp
tag_modelpath = konlp.__path__[0] + "/tag/kmou/data/"
token_modelpath = konlp.__path__[0] + "/tokenize/kmou/data/"
@pytest.fixture
def input_string():
    return '가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'


def test_SentenceTokenizer():
    ST=SentenceTokenizer()
    assert ST.pyt_sent_tokenizer('아버지가 방에 들어간다. 학교는 잠을 자는 곳이 아니라 공부하는 곳이다.') == ['아버지가 방에 들어간다.', '학교는 잠을 자는 곳이 아니라 공부하는 곳이다.']


def test_WordSegment():
    WS = WordSegment()
    WS.set_model_file(token_modelpath+"SPACE.crf.model")
    assert WS.tag("아버지가방에들어간다") == "아버지가 방에 들어간다."


def test_VXP_ChunkTagger(input_string):
    vxp = VXP_ChunkTagger()
    vxp.set_chunk_rule(tag_modelpath+"ChunkingRule_VXP.txt")
    assert vxp.tag(input_string) == '가게/NNG+에서/JKB 사/VV+아_가지/VXP+고_가/VXP+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'


def test_JSP_ChunkTagger(input_string):
    jsp = JSP_ChunkTagger()
    jsp.set_chunk_rule(tag_modelpath+"ChunkingRule_JSP.txt")
    assert jsp.tag(input_string) == '가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에_대하_어서는/JSP 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'


def test_NERTagger():
    NERT = NERTagger()
    NERT.set_model_file(tag_modelpath+"NER.crfsuite")
    assert NERT.tag("박용운씨는 사람이다.") == [('박', 'B-PER'), ('용', 'I-PER'), ('운', 'I-PER'), (' ', 'O'), ('씨', 'O'), ('는', 'O'), (' ', 'O'), ('사', 'O'), ('람', 'O'), ('이', 'O'), ('다', 'O'), ('.', 'O')]
