import pytest
from konlp.chat.indexer_extractor import IndexerExtractor

extractor = IndexerExtractor()
def test_idx_extractor_with_original_form():
    str = '철수와 영희는 영화를 본다.'
    idx_term, with_original_form = extractor.indexer_extract(str, True)
    assert idx_term == ['철수/NNP @PER', '영희/NNP @PER', '영화/NNG', '보/VV']
    assert with_original_form == ['철수/NNP @PER', '영희/NNP @PER', '영화/NNG 영화/NNG', '보/VV 보/VV']

def test_idx_extractor():
    str = '철수와 영희는 영화를 본다.'
    idx_term, with_original_form = extractor.indexer_extract(str, False)
    assert idx_term == ['철수/NNP @PER', '영희/NNP @PER', '영화/NNG', '보/VV']
    assert with_original_form is None

