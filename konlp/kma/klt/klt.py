# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - klt
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#         HyunYoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""Klt 한국어 형태소 분석기

klt에 대한 정보는 http://nlp.kookmin.ac.kr/HAM/kor/index.html에서 참조하면 됩니다.

현재 klt는 analyze, tokens, nouns 기능을 제공합니다.
모든 기능을 사용하기 위해서는 dictionary를 초기화해야합니다.
dictionary는 konlp설치시 konlp의 dist-pacakge에 설치가 됩니다.
기본 dictionary파일들은 klt모듈을 쓸 때 자동으로 초기화가 됩니다.
만약 다른 위치에 있으면 dic_init함수를 써서 초기화하면 됩니다.

Example:
    >>> from  konlp.kma import KltKma
    >>> k = KltKma()
    >>> simple_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> simple_txt2 = "국민대학교자연어처리연구실"
    >>> k.analyze(simple_txt)
    [('안녕하세요', [('안녕', 'N'), ('하', 't'), ('세요', 'e')]),
    ('.', [('.', 'q')]), ('국민대학교', [('국민대학교', 'N')]),
    ('자연어처리', [('자연어처리', 'N')]),
    ('연구실입니다', [('연구실', 'N'), ('이', 'c'), ('습니다', 'e')]),
    ('.', [('.', 'q')])]
    >>> k.tokens(simple_txt)
    ['안녕', '하', '세요', '.', '국민대학교', '자연어처리', '연구실', '이', '습니다', '.']
    >>> k.nouns(simple_txt)
    ['안녕', '국민대학교', '자연어처리', '연구실']
    >>> k.cnouns(simple_txt2)
    ['국민', '대학교', '자연어', '처리', '연구실']

TODO:
    We will change functionality with Cython

"""
# for load libindex.so.3
from ctypes import cdll

# load libindex.so.3
# Later on we will change the method to load the libindex.so.3
import konlp
cdll.LoadLibrary(konlp.__path__[0] + "/kma/klt/lib/libindex.so.3")

# libindex.so.3 파일을 먼저 load해야하기 때문에 pylint disable을 했습니다.
from konlp.kma.api import KmaI
from konlp.kma.klt.lib import kma  as _kma  # pylint: disable = no-name-in-module
# we change the way to import index with cython
from konlp.kma.klt.lib import index as _index # pylint: disable = no-name-in-module

class KltKma(KmaI):
    """Klt 한국어 형태소 분석기

    klt에 대한 정보는 http://nlp.kookmin.ac.kr/HAM/kor/index.html에서 참조하면 됩니다.

    Example:
        >>> from  konlp.kma import KltKma
        >>> k = KltKma()
        >>> simple_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
        >>> simple_txt2 = "국민대학교자연어처리연구실"
        >>> k.analyze(simple_txt)
        [('안녕하세요', [('안녕', 'N'), ('하', 't'), ('세요', 'e')]),
        ('.', [('.', 'q')]), ('국민대학교', [('국민대학교', 'N')]),
        ('자연어처리', [('자연어처리', 'N')]),
        ('연구실입니다', [('연구실', 'N'), ('이', 'c'), ('습니다', 'e')]),
        ('.', [('.', 'q')])]
        >>> k.tokens(simple_txt)
        ['안녕', '하', '세요', '.', '국민대학교', '자연어처리', '연구실', '이', '습니다', '.']
        >>> k.nouns(simple_txt)
        ['안녕', '국민대학교', '자연어처리', '연구실']
        >>> k.cnouns(simple_txt2)
        ['국민', '대학교', '자연어', '처리', '연구실']

    """

    def __init__(self):
        """Klt module's __init__ method

        Args:
            dic_path(str): 사전 위치

        """
        self.dic_path = konlp.__path__[0] + "/kma/klt/data/"
        self.dic_init(self.dic_path)

    def dic_init(self, dic_path=""):
        """사전을 초기화하는 함수입니다.

        Args:
            dic_path(str): 사전 위치

        """
        if dic_path == "":
            dic_path = self.dic_path
        _kma.init(dic_path)
        _index.init(dic_path)

    def analyze(self, sentence):
        """문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        Args:
            sentence(str): 형태소/품사 분석한 문장

        Returns:
            (원본, [(형태소, 품사)]) list

        """
        return _kma.morpha(sentence)[1]

    def tokens(self, sentence):
        """문장을 입력받아 형태소만 출력합니다.

        Args:
            sentence(str): 형태소를 분석한 문장

        Returns:
            형태소 분석된 list

        """
        morpha = _kma.morpha(sentence)[1]

        list_morphs = []

        for i in morpha:
            for j in i[1]:
                list_morphs.append(j[0])

        return list_morphs

    def nouns(self, sentence):
        """문장을 입력받아 색인어들을 출력합니다.

        Args:
            sentence(str): 색인어 추출한 문장

        Returns:
            색인어가 추출된 list

        """
        result_of_index = _index.index(sentence)

        list_nouns = []

        for i in result_of_index:
            if i[1]:
                list_nouns.append(i[1][0])

        return list_nouns

    def cnouns(self, string): # pylint: disable=no-self-use
        """복합명사를 입력받아 복합명사 분해를 합니다.

        Args:
            string(str): 복합명사

        Returns:
            복합명상 분해된 list

        """
        return _index.noun_comp(string, " ")
