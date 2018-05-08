# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Klt 형태소 분석기 for Korean Natural Language Toolkit
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Hyunyoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
from konlp.chat.pseudo_morpeme_analyzer import PseudoMorphemeAnalyzer
from konlp.chat.pseudo_morpeme_analyzer import config


def input_list():
    return "안녕하세요. 강원대학교 자연어처리 연구실입니다."


def road_pas_model():
    psa = PseudoMorphemeAnalyzer(config.MORPHEME_ANALYSIS_MODEL)
    return psa


def test_analyze(input_line, psa):
    assert psa.analyze(input_line)

