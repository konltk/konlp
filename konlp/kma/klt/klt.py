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
"""
Klt 한국어 형태소 분석기

klt 한국어 형태소 분석기는 국민대학교 강승식 교수님이 만든 형태소 분석기 입니다.
더 많은 정보를 보실려면 http://nlp.kookmin.ac.kr/HAM/kor/index.html 에서 보시면 됩니다.

현재 klt는 analyze, morphs, nouns 기능을 제공합니다.
모든 기능을 사용하기 위해서는 dictionary를 초기화해야합니다.
dictionary는 konlp설치시 konlp의 dist-pacakge에 설치가 됩니다.
기본 dictionary파일들은 klt모듈을 쓸 때 자동으로 초기화가 됩니다.
만약 다른 위치에 있으면 dic_init함수를 써서 초기화하면 됩니다.

Example:
    >>> from konlp.kma.klt import klt
    >>> k = klt.KltKma()
    >>> simple_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> k.analyze(simple_txt)
    [('안녕하세요', [('안녕', 'N'), ('하', 't'), ('세요', 'e')]), ('.', [('.', 'q')]),
    ('국민대학교', [('국민대학교', 'N')]), ('자연어처리', [('자연어처리', 'N')]), ('연구실입니다',
    [('연구실', 'N'), ('이', 'c'), ('습니다', 'e')]), ('.', [('.', 'q')])]
    >>> k.morphs(simple_txt)
    ['안녕', '하', '세요', '.', '국민대학교', '자연어처리', '연구실', '이', '습니다', '.']
    >>> k.nouns(simple_txt)
    ['안녕', '국민대학교', '자연어처리', '연구실']
"""
# for load libindex.so.3
from ctypes import cdll

# load libindex.so.3
# Later on we will change the method to load the libindex.so.3 
import konlp
cdll.LoadLibrary(konlp.__path__[0] + "/kma/klt/lib/libindex.so.3")

# libindex.so.3 파일을 먼저 load해야하기 때문에 pylint disable을 했습니다.
from konlp.kma.api import KmaI # pylint: disable=C0413
from konlp.kma.klt.lib import kma  as _kma # pylint: disable=C0413
# we change the way to import index with cython 
from konlp.kma.klt.lib import index as _index # pylint: disable=C0413

class KltKma(KmaI):
    """
    국민대학교 강승식 교수님의 KLT2000입니다
    """

    def __init__(self):
        """
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
        _kma.init(dic_path) # pylint: disable=I1101
        _index.init(dic_path) # pylint: disable=I1101

    def analyze(self, _input):
        """문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        Args:
            _input(str): 형태소/품사 분석한 문장

        Returns:
            (원본, [(형태소, 품사)]) list
        """
        return _kma.morpha(_input)[1] # pylint: disable=I1101

    def morphs(self, _input):
        """문장을 입력받아 형태소만 출력합니다.

        Args:
            _input(str): 형태소를 분석한 문장

        Returns:
            형태소 분석된 list
        """
        morpha = _kma.morpha(_input)[1] # pylint: disable=I1101

        list_morphs = []

        for i in morpha:
            for j in i[1]:
                list_morphs.append(j[0])

        return list_morphs

    def nouns(self, _input):
        """문장을 입력받아 색인어들을 출력합니다.

        Args:
            _input(str): 색인어 추출한 문장

        Returns:
            색인어가 추출된 list
        """
        result_of_index = _index.index(_input) # pylint: disable=I1101

        list_nouns = []

        for i in result_of_index:
            if i[1]:
                list_nouns.append(i[1][0])

        return list_nouns

    def noun_comp(self, _input): # pylint: disable=R0201
        """복합명사를 입력받아 복합명사 분해를 합니다.

        Args:
            _input(str): 부해한 복합명사

        Returns:
            복합명상 분해된 list
        """
        return _index.noun_comp(_input, " ") # pylint: disable=I1101
