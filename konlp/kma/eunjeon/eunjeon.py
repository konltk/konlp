# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - eunjeon
#
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""seunjeon 한국어 형태소 분석기

이 코드는 자바로 된 seunjeon 형태소 분석기를 Python으로 wrapping한 코드입니다.
seunjeon 형태소 분석기는 은전한닢(http://eunjeon.blogspot.kr/)에서 만들어졌습니다.
더 많은 정보를 보실려면 http://eunjeon.blogspot.kr/ 에서 보시면 됩니다.
현재 seunjeon는 analyze, morphs, nouns, set_user_dict 기능을 제공합니다.
기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
    $ sudo apt-get install openjdk-8-jdk
그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
    $ sudo pip3 install JPype1-py3

Example:
    >>> from konlp.kma.eunjeon import eunjeon
    >>> ej = eunjeon.Eunjeon()
    >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> ej.analyze(simple_text)
    [('안녕', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF'), ('.', 'SF'), ('국민대', 'NNP'), ('학교', 'NNG'),
    ('자연어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('입니다', 'VCP+EF'), ('.', 'SF')]
    >>> ej.morphs(simple_text)
    ['안녕', '하', '세요', '.', '국민대', '학교', '자연어', '처리', '연구실', '입니다', '.']
    >>> ej.nouns(simple_text)
    ['안녕', '국민대', '학교', '자연어', '처리', '연구실']
"""

from konlp.kma.api import KmaI

import os
import jpype


class Eunjeon(KmaI):
    """seunjeon 한국어 형태소 분석기

    현재 seunjeon는 analyze, morphs, nouns, set_user_dict 기능을 제공합니다.
    기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
        $ sudo apt-get install openjdk-8-jdk
    그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
        $ sudo pip3 install JPype1-py3
    """
    def __init__(self):
        self._jvm_init()
        self.eunjeon = jpype.JPackage('org.bitbucket.eunjeon.seunjeon')
        self.COMPOUND = 'compound'
        self.INFLECT = 'inflect'

    def _jvm_init(self):
        """jvm init method for eunjeon

        자바로 된 eunjeon을 사용하기 위해서 jvm 설정과 시작을 합니다.
        파이썬 패키지 'JPype', 그리고 jdk가 설치되어 있어야 합니다.
        """
        if jpype.isJVMStarted():
            jpype.shutdownJVM()

        jvm_path = jpype.getDefaultJVMPath()

        cur_dir = os.path.dirname(__file__)
        lib_dir = os.path.join(cur_dir, 'lib')
        jar_list = os.listdir(lib_dir)
        class_path = ':'.join(os.path.join(lib_dir, jar) for jar in jar_list)

        jpype.startJVM(jvm_path, '-Djava.class.path={}'.format(class_path))

    def set_user_dict(self, user_list):
        """사용자 사전 추가

        user_list를 사용하여 사용자 사전을 구축합니다.
        user_list는 단어들로 구성되어 있고 각 단어는 str 타입입니다.
        각 단어는 'surface, cost'로 구성합니다. (cost는 생략해도 관계없음)
        - surface : 단어명, '+' 문자를 사용해서 복합 명사를 구성할 수 있습니다. '+' 문자 자체는 '\+' 를 이용합니다.
        - cost : 단어 출현 비용, 작을수록 출현 확률이 높습니다.

        Examples:
            >>> from konlp.kma import Eunjeon
            >>> ej = Eunjeon()
            >>> ej.analyze('C++')
            [('C', 'SL'), ('+', 'SY'), ('+', 'SY')]
            >>> ej.set_user_dict(['C\+\+'])
            >>> ej.analyze('C++')
            [('C++', 'NNG')]

        Args:
            user_list(list): str 타입으로 구성된 단어들의 리스트
        """
        array_list = jpype.java.util.ArrayList()

        for word in user_list:
            array_list.add(jpype.java.lang.String(word))

        self.eunjeon.Analyzer.setUserDict(array_list.iterator())

    def analyze(self, string, **kwargs):
        """형태소 분석 함수

        문장(string) 을 입력받아 형태소 분석을 진행합니다. 3가지의 옵션을 가집니다.
        1. compress : 압축모드 분석(heap memory 사용 최소화. 속도는 상대적으로 느림.)
        2. inflect : 활용어 원형
        3. compound : 복합명사 분해

        Examples:
            >>> from konlp.kma import Eunjeon
            >>> ej = Eunjeon()
            >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
            >>> ej.analyze(simple_text)
            [('안녕', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF'), ('.', 'SF'), ('국민대', 'NNP'), ('학교', 'NNG'),
            ('자연어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('입니다', 'VCP+EF'), ('.', 'SF')]
            >>> ej.analyze(simple_text, inflect=True)
            [('안녕', 'NNG'), ('하', 'XSV'), ('시', 'EP'), ('.', 'SF'), ('국민대', 'NNP'), ('학교', 'NNG'),
            ('자연어', 'NNG'), ('처리', 'NNG'), ('연구실', 'NNG'), ('이', 'VCP'), ('ᄇ니다', 'EF'), ('.', 'SF')]
            >>> ej.analyze(simple_text, inflect=True, compound=True)
            [('안녕', 'NNG'), ('하', 'XSV'), ('시', 'EP'), ('.', 'SF'), ('국민', 'NNG'), ('대', 'NNG'),
            ('학교', 'NNG'), ('자연', 'NNG'), ('어', 'NNG'), ('처리', 'NNG'), ('연구', 'NNG'), ('실', 'NNG'),
            ('이', 'VCP'), ('ᄇ니다', 'EF'), ('.', 'SF')]

        Args:
            string (str): 형태소 분석할 문장
            **kwargs: (compress, inflect, compound) option

        Returns:
            list: 형태소 리스트
        """
        if 'compress' in kwargs and kwargs['compress'] == True:
            arr = self.eunjeon.CompressedAnalyzer.parseJava(string).toArray()
        else:
            arr = self.eunjeon.Analyzer.parseJava(string).toArray()

        parse_list = []

        for item in arr:
            m = item.morpheme()
            m_type = str(m.mType).lower()

            if m_type == self.COMPOUND and self.COMPOUND in kwargs and kwargs[self.COMPOUND] == True:
                for element in item.deCompoundJava().toArray():
                    m = element.morpheme()
                    parse_list.append((m.surface, m.featureHead))

            elif m_type == self.INFLECT and self.INFLECT in kwargs and kwargs[self.INFLECT] == True:
                for element in item.deInflectJava().toArray():
                    m = element.morpheme()
                    parse_list.append((m.surface, m.featureHead))

            else:
                m = item.morpheme()
                parse_list.append((m.surface, m.featureHead))

        return parse_list

    def morphs(self, string, **kwargs):
        """형태소 추출 함수

        문장(string) 을 입력받아 형태소만 추출합니다. analyze 함수처럼 3가지의 옵션을 가집니다.
        1. compress : 압축모드 분석(heap memory 사용 최소화. 속도는 상대적으로 느림.)
        2. inflect : 활용어 원형
        3. compound : 복합명사 분해

        Examples:
            >>> from konlp.kma import Eunjeon
            >>> ej = Eunjeon()
            >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
            >>> ej.morphs(simple_text)
            ['안녕', '하', '세요', '.', '국민대', '학교', '자연어', '처리', '연구실', '입니다', '.']
            >>> ej.morphs(simple_text, inflect=True)
            ['안녕', '하', '시', '.', '국민대', '학교', '자연어', '처리', '연구실', '이', 'ᄇ니다', '.']
            >>> ej.morphs(simple_text, inflect=True, compound=True)
            ['안녕', '하', '시', '.', '국민', '대', '학교', '자연', '어', '처리', '연구', '실', '이', 'ᄇ 니다', '.']

        Args:
            string (str): 형태소를 추출할 문장
            **kwargs: (compress, inflect, compound) option

        Returns:
            list: 형태소 리스트
        """
        parse_list = self.analyze(string, **kwargs)
        morph_list = [item[0] for item in parse_list]

        return morph_list

    def nouns(self, string, **kwargs):
        """명사 추출 함수

        문장(string) 을 입력받아 명사를 추출합니다. analyze 함수처럼 3가지의 옵션을 가집니다.
        1. compress : 압축모드 분석(heap memory 사용 최소화. 속도는 상대적으로 느림.)
        2. inflect : 활용어 원형
        3. compound : 복합명사 분해

        Examples:
            >>> from konlp.kma import Eunjeon
            >>> ej = Eunjeon()
            >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
            >>> ej.nouns(simple_text)
            ['안녕', '국민대', '학교', '자연어', '처리', '연구실']
            >>> ej.nouns(simple_text, compound=True)
            ['안녕', '국민', '대', '학교', '자연', '어', '처리', '연구', '실']

        Args:
            string (str): 명사를 추출할 문장
            **kwargs: (compress, inflect, compound) option

        Returns:
            list: 명사 리스트
        """

        parse_list = self.analyze(string, **kwargs)
        noun_list = [item[0] for item in parse_list if item[1].startswith('N') ]

        return noun_list
