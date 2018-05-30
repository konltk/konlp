# -*- coding : utf-8 -*-

import pytest
from konlp.kma.indexer_extractor import IndexerExtractor

extractor = IndexerExtractor()

query = "밥이 먹고 싶다."
idx_term = extractor.analyze(query)
print(idx_term)
idx_term = extractor.morphs(query)
print(idx_term)
idx_term = extractor.nouns(query)
print(idx_term)


@pytest.fixture
def test_analyze():
    str = "밥이 먹고 싶다."
    result = extractor.analyze(str)
    assert result == ['밥/NNG', '먹/VV', 'M#34']

@pytest.fixture
def test_tokens():
    str = "밥이 먹고 싶다."
    result = extractor.morphs(str)
    assert result == ['밥/NNG', '먹/VV', '고/EC 싶/VX']

@pytest.fixture
def test_nouns():
    str = "밥이 먹고 싶다."
    result = extractor.nouns(str)
    assert result == ['밥/NNG']


test_analyze()
test_tokens()
test_nouns()