# -*- coding : utf-8 -*-

import pytest
from konlp.kma.indexer_extractor import IndexerExtractor

extractor = IndexerExtractor()

def test_analyze():
    str = "밥이 먹고 싶다."
    result = extractor.analyze(str)
    assert result == ['밥/NNG', '먹/VV', 'M#34']

def test_tokens():
    str = "밥이 먹고 싶다."
    result = extractor.tokens(str)
    assert result == ['밥/NNG', '먹/VV', '고/EC 싶/VX']

def test_nouns():
    str = "밥이 먹고 싶다."
    result = extractor.nouns(str)
    assert result == ['밥/NNG']


test_analyze()
test_tokens()
test_nouns()
