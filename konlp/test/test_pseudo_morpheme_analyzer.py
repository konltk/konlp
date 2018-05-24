# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Autospacing of klt
#
# Author: Younghun Cho <cyh905@gmail.com>
#         HyunYoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import pytest
from konlp.kma.pseudo_morpheme_analyzer import PseudoMorphemeAnalyzer
from konlp.kma.pseudo_morpheme_analyzer import config

@pytest.fixture
def test_pseudo_morp_analyzer():
    analyzer = PseudoMorphemeAnalyzer(config.MORPHEME_ANALYSIS_MODEL)
    str = '철수와 영희는 영화를 본다.'
    assert analyzer.analyze(str) == ['철수/NNP + 와/JC', '영희/NNP + 는/JX', '영화/NNG + 를/JKO', '보/VV + ㄴ다/EF + ./SF']

test_pseudo_morp_analyzer()
