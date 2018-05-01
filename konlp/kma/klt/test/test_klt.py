# -*- encode: utf8 -*-
import pytest
from konlp.kma.klt import klt

@pytest.fixture
def input_list():
    return "안녕하세요"

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