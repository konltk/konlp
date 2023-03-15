# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - komoran
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""komoran 한국어 형태소 분석기

이 코드는 자바로 된 komoran 형태소 분석기를 Python으로 wrapping한 코드입니다.
komoran 형태소 분석기는 Shineware(http://www.shineware.co.kr/about/shineware/)에서 만들어졌습니다.
더 많은 정보를 보실려면 http://shineware.tistory.com/entry/KOMORAN-ver-24 에서 보시면 됩니다.

현재 komoran는 analyze, morphs, nouns 기능을 제공합니다.
기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
    $ sudo apt-get install openjdk-8-jdk
그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
    $ sudo pip3 install JPype1-py3

Example:
    >>> from konlp.kma.komoran import komoran
    >>> km = komoran.Komoran()
    >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> km.analyze(simple_text)
    [('안녕', 'NNG'), ('하', 'XSV'), ('시', 'EP'), ('어요', 'EF'),
    ('.', 'SF'), ('국민', 'NNG'), ('대학교', 'NNG'), ('자연', 'NNG'),
    ('어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('이', 'VCP'),
    ('ㅂ니다', 'EF'), ('.', 'SF')]
    >>> km.morphs(simple_text)
    ['안녕', '하', '시', '어요', '.','국민', '대학교', '자연', '어', '처리',
    '연구실', '이', 'ㅂ니다', '.']
    >>> km.nouns(simple_text)
    ['안녕', '국민', '대학교', '자연', '어', '처리', '연구실']
"""
import jpype
import konlp
from konlp.kma.api import KmaI


class Komoran(KmaI):
    """komoran 한국어 형태소 분석기

    현재 komoran는 analyze, morphs, nouns 기능을 제공합니다.
    기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
        $ sudo apt-get install openjdk-8-jdk
    그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
        $ sudo pip3 install JPype1-py3

    Example:
        >>> from konlp.kma.komoran import komoran
        >>> km = komoran.Komoran()
        >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
        >>> km.analyze(simple_text)
        [('안녕', 'NNG'), ('하', 'XSV'), ('시', 'EP'), ('어요', 'EF'),
        ('.', 'SF'), ('국민', 'NNG'), ('대학교', 'NNG'), ('자연', 'NNG'),
        ('어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('이', 'VCP'),
        ('ㅂ니다', 'EF'), ('.', 'SF')]
        >>> km.morphs(simple_text)
        ['안녕', '하', '시', '어요', '.','국민', '대학교', '자연', '어', '처리',
        '연구실', '이', 'ㅂ니다', '.']
        >>> km.nouns(simple_text)
        ['안녕', '국민', '대학교', '자연', '어', '처리', '연구실']
    """

    _JAR = ['komoran-2.4-e.jar', 'shineware-common-2.0.jar', 'shineware-ds-1.0.jar']

    def __init__(self, dic_path=None, full=False, jvm_path=None):
        """init funtion for Komoran

        자바로 된 Komoran를 사용하기 위해서 jvm 설정과 시작을 합니다.
        파이썬 패키지 'JPype', 그리고 jdk가 설치되어 있어야 합니다.

        Args:
            dic_path(str): 형태소 분석에 필요한 사전 파일 경로
            full(bool): 사전의 종류(full, light) 중 full을 사용할 변수
            jvmpath(str): jvm의 경로
        """
        file_path = konlp.__path__[0] + "/kma/komoran/lib/"
        class_path = ":".join(file_path+i for i in self._JAR)
        jvm_path = jvm_path or jpype.getDefaultJVMPath()
        if jvm_path and not jpype.isJVMStarted():
            jpype.startJVM(jvm_path, '-Djava.class.path=%s' % class_path,
                           '-Dfile.encoding=UTF8',
                           '-ea', '-Xmx1024m')

        self.dic_init(dic_path, full)

    def dic_init(self, dic_path=None, full=False):
        """사전을 초기화하는 함수입니다.

        Args:
            dic_path(str): 사전 위치
            full(bool): 사전의 종류(full, light) 중 full을 사용할 변수
        """
        if not dic_path:
            dic_path = konlp.__path__[0] + "/kma/komoran/data/"
            dic_path += "models-full" if full else "models-light"

        self.dic_path = dic_path


    def analyze(self, string):
        """형태소 분석기

        문장을 입력받아 형태소 분석을 합니다.

        Args:
            string(str): 형태소/품사 분석할 문장

        Returns:
            [(형태소, 품사), ] list
        """
        komo = jpype.JPackage('kr.co.shineware.nlp.komoran.core.analyzer').Komoran(self.dic_path)
        result = komo.analyze(string)

        r_l = []
        for i in range(result.size()):
            eojeol = result.get(i)
            for j in range(eojeol.size()):
                morph = eojeol.get(j)
                r_l.append((morph.getFirst(), morph.getSecond()))

        return r_l

    def morphs(self, string):
        """형태소 분리

        형태소 분석 후에 분리된 형태소만 얻는 함수 입니다.

        Args:
            string(str): 형태소 분리할 문장

        Returns:
            분리된 형태소의 list
        """
        komo = jpype.JPackage('kr.co.shineware.nlp.komoran.core.analyzer').Komoran(self.dic_path)
        result = komo.analyze(string)

        r_l = []
        for i in range(result.size()):
            eojeol = result.get(i)
            for j in range(eojeol.size()):
                morph = eojeol.get(j)
                r_l.append(morph.getFirst())

        return r_l

    def nouns(self, string):
        """단어 추출기

        문장을 입력받아 단어를 추출합니다.

        Args:
            string(str): 단어 추출할 문장

        Returns:
            단어가 추출된 list
        """
        import re
        komo = jpype.JPackage('kr.co.shineware.nlp.komoran.core.analyzer').Komoran(self.dic_path)
        result = komo.analyze(string)

        r_l = []
        for i in range(result.size()):
            eojeol = result.get(i)
            for j in range(eojeol.size()):
                morph = eojeol.get(j)
                if re.search("NN.*", morph.getSecond()):
                    r_l.append(morph.getFirst())

        return r_l
