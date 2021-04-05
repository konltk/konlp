# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - klt for jvm
#
#
# Author: Jungmin Kim <ty911007@naver.com>
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

Example:
    >>> from  konlp.kma import Jklt
    >>> k = Jklt()
    >>> simple_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> simple_txt2 = "국민대학교자연어처리연구실"
    >>> k.analyze(simple_txt)
    [('안녕하', 'V'), ('세요', 'E'), ('국민대학교', 'N'), 
    ('자연어처리', 'N'), ('연구실', 'N'), ('B니다', 'E')]
    >>> k.tokens(simple_txt)
    ['안녕하', '세요', '국민대학교', '자연어처리', '연구실', 'B니다']
    >>> k.nouns(simple_txt)
    ['국민대학교', '자연어처리', '연구실'] 
"""

import jpype
import json
import os
import sys

from konlp.kma.api import KmaI


class Jklt(KmaI):
    def __init__(self):
        """Klt module's __init__ method

        Args:
            dic_path(str): 사전 위치

        """
        import konlp
        # path = os.path.dirname(os.path.abspath(__file__))
        classpath = os.pathsep.join([konlp.__path__[0] + "/kma/kkma/lib/" + "kkma-2.0.jar",konlp.__path__[0] + "/kma/jklt/lib/" + "Kma.jar"])
        
        if not jpype.isJVMStarted():
            jpype.startJVM(
                jpype.getDefaultJVMPath(),
                "-Djava.class.path={classpath}".format(classpath=classpath)
            )
        jpkg = jpype.JPackage("HamPack.Run")
        self.kma = jpkg.Morphs(konlp.__path__[0] + "/kma/jklt/hdic/")
        print(konlp.__path__[0] + "/kma/jklt/hdic/")

    def analyze(self, string):
        """문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장

        Returns:
            list(list(str)): 형태소 후보군들 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        result = []
        for word in self.kma.pos(string):
           word = word[1:len(word)-1]

           w = word.split(',')

           temp = (w[0],w[1])

           result.append(temp)
        
        return result

    def tokens(self, string):
        """문장을 입력받아 형태소만 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장

        Returns:
            list(str): 형태소 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        return list(self.kma.getToken(string))

    def nouns(self, string):
        """문장을 입력받아 색인어들을 출력합니다.

        Args:
            string (str): 색인어를 추출할 문장

        Returns:
            list(str): 색인어 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        return list(self.kma.getNouns(string))

    def options(self,options):
        """token추출시 형태소 분석 옵션을 설정할수 있습니다.

        Args:
            options (dictionary): 설정할 옵션들의 Dictionary, key : str, value : bool
            syl_1	// 1음절 명사 추출시
			verbs	// 동사, 형용사, 부사 등 추출시
			syl_9	// 9음절 이상인 명사 제거
			at_sp	// 자동띄어쓰기 기능 적용
			ns_cn	// 제목에 대한 자동띄어쓰기 기능
			ascii	// 영문자, 숫자가 포함된 것 추출
			anorm	// 숫자와 한글이 혼합된 숫자를 아라비아 숫자로 변환
			cnoun	// 복합명사를 분해하지 않음
			cnn_2	// 복합명사 분해시 이웃한 2 명사들을 조합하여 출력
									// '정보검색시스템' --> '정보검색', '검색시스템'도 출력
			stopw	// 불용어를 제거하지 않음
			key1	// 명사+'하다/되다/스럽다'는 추출하지 않음
			key2	// 복합명사와 미등록어만 추출시
            
        """
        self.kma.setOption(options)