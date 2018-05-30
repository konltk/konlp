# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean automatic word spacing
#
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""한국어 자동 띄어쓰기 프로그램

KmuAsp 는 한국어 문장에 대해 자동 띄어쓰기를 수행합니다.
tensorflow로 Bi-LSTM-CRF 모델을 구현하여 학습을 진행하였습니다.

Example:
    >>> from konlp.tokenize import KmuAsp
    >>> asp = KmuAsp()
    >>> asp.tokenize('국민대자연어처리연구실입니다.')
    ['국민대 자연어처리 연구실입니다.']
    >>> asp.tokenize_sents(['국민대자연어처리연구실입니다.', '나는밥을먹고학교에갔다.'])
    ['국민대 자연어처리 연구실입니다.', '나는 밥을 먹고 학교에 갔다.']
"""

from konlp.tokenize.api import TokenizerI
from konlp.tokenize.kmuasp.model import BiLSTMCRF


class KmuAsp(TokenizerI):
    """한국어 자동 띄어쓰기 프로그램

    KmuAsp 는 한국어 문장에 대해 자동 띄어쓰기를 수행합니다.
    tensorflow로 Bi-LSTM-CRF 모델을 구현하여 학습을 진행하였습니다.

    Example:
        >>> from konlp.tokenize import KmuAsp
        >>> asp = KmuAsp()
        >>> asp.tokenize('국민대자연어처리연구실입니다.')
        ['국민대 자연어처리 연구실입니다.']
        >>> asp.tokenize_sents(['국민대자연어처리연구실입니다.', '나는밥을먹고학교에갔다.'])
        ['국민대 자연어처리 연구실입니다.', '나는 밥을 먹고 학교에 갔다.']
    """
    def __init__(self):
        self.model = BiLSTMCRF()

    def tokenize(self, string):
        """문장에 대해서 자동 띄어쓰기를 수행합니다. 
        
        문장을 입력받으면 모든 공백을 제거한 뒤, 자동 띄어쓰기를 수행합니다. 
        
        Args:
            string (str): 문장  

        Returns:
            str: 띄어쓰기가 된 문장 
        """
        return self.model.tokenize([string])

    def tokenize_sents(self, sents):
        """문장들에 대해서 자동 띄어쓰기를 수행합니다. 

        문장들을 입력받으면 모든 공백을 제거한 뒤, 자동 띄어쓰기를 수행합니다. 

        Args:
            sents (list): 문장들의 리스트 

        Returns:
            list: 띄어쓰기가 된 문장들 리스트
        """
        return self.model.tokenize(sents)
