# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean morpheme analyzer - kkma
#
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Hyunyoung Lee <hyun02.engineer@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""kkma 한국어 형태소 분석기

이 코드는 꼬꼬마 형태소 분석기를 Python으로 wrapping한 코드입니다.
꼬꼬마 형태소 분석기는 서울대학교 IDS(intelligent Data Systems)에서 만들어졌습니다.
더 많은 정보를 보실려면 http://kkma.snu.ac.kr/ 에서 보시면 됩니다.

현재 kkma는 analyze, morphs, nouns 기능을 제공합니다.
기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
    $ sudo apt-get install openjdk-8-jdk

그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
    $ sudo pip3 install JPype1-py3

Example:
    >>> from konlp.kma import Kkma
    >>> kk = Kkma()
    >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> kk.analyze(simple_text)
    [['안녕하세요.', ['안녕/NNG', '하/XSV', '세요/EFN', './SF']],
    ['국민대학교 자연어처리 연구실입니다.',
    ['국민대학교/NNG', '자연어/NNG', '처리/NNG', '연구실/NNG',
    '이/VCP', 'ㅂ니다/EFN', './SF']]]
    >>> kk.morphs(simple_text)
    ['안녕', '하', '세요', '.', '국민대학교',
    '자연어', '처리', '연구실', '이', 'ㅂ니다', '.']
    >>> kk.nouns(simple_text)
    ['안녕', '국민', '국민대학교', '대학교',
    '자연어', '자연어처리', '처리', '연구실']

TODO : The way to initialize JVM have to change

"""
import os
import konlp
import sys
import platform
if platform.system() == 'Windows':
    sys.path = [konlp.__path__[0] + '/lib_win'] + sys.path
import jpype as jp#import jpype as jp # pylint: disable=import-error
from konlp.kma.api import KmaI

class Kkma(KmaI):
    """서울대학교 IDS에서 만들어진 꼬꼬마 형태소 분석기입니다.

    기능을 사용하기 전에는 pc에 jdk(8 or older)가 설치되어 있어야 합니다.
        $ sudo apt-get install openjdk-8-jdk

    그리고 또한 파이썬 패키지인 JPype가 설치되어 있어야 합니다.
        $ sudo pip3 install JPype1-py3

    Example:
        >>> from konlp.kma import Kkma
        >>> kk = Kkma()
        >>> simple_text = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
        >>> kk.analyze(simple_text)
        [['안녕하세요.', ['안녕/NNG', '하/XSV', '세요/EFN', './SF']],
        ['국민대학교 자연어처리 연구실입니다.',
        ['국민대학교/NNG', '자연어/NNG', '처리/NNG', '연구실/NNG',
        '이/VCP', 'ㅂ니다/EFN', './SF']]]
        >>> kk.morphs(simple_text)
        ['안녕', '하', '세요', '.', '국민대학교',
        '자연어', '처리', '연구실', '이', 'ㅂ니다', '.']
        >>> kk.nouns(simple_text)
        ['안녕', '국민', '국민대학교', '대학교',
        '자연어', '자연어처리', '처리', '연구실']

    """

    def __init__(self, jvmpath=None):
        """init funtion for Kkma

        자바로 된 kkma를 사용하기 위해서 jvm 설정과 시작을 합니다.
        파이썬 패키지 'JPype', 그리고 jdk가 설치되어 있어야 합니다.

        Args:
            jvmpath(str): jvm의 경로

        """
        import konlp
        classpath = os.pathsep.join([konlp.__path__[0] + "/kma/kkma/lib/" + "kkma-2.0.jar",konlp.__path__[0] + "/kma/klt2000/lib/" + "klt2000.jar"])
        jvmpath = jvmpath or jp.getDefaultJVMPath()
        if jvmpath and not jp.isJVMStarted():
            jp.startJVM(jvmpath, '-Djava.class.path=%s' % classpath,
                        '-Dfile.encoding=UTF8',
                        '-ea', '-Xmx1024m')
        # else:
            # raise ValueError("There is no JVM Path.")


    def nouns(self, string):
        """단어 추출기

        문장을 입력받아 단어를 추출합니다.

        Args:
            string(str): 단어 추출할 문장

        Returns:
            단어가 추출된 list

        """
        j_p = jp.JPackage('org.snu.ids.ha.index')
        key_l = j_p.KeywordExtractor().extractKeyword(string, True)
        result_list = []
        for i in range(key_l.size()):
            result_list.append(key_l.get(i).getString())
        return result_list

    def analyze(self, string):
        """형태소 분석기

        문장을 입력받아 형태소 분석을 합니다.

        Args:
            string(str): 형태소/품하 분석할 문장

        Returns:
            [[원본, [형태소/품사]]]

        """
        j_p = jp.JPackage('org.snu.ids.ha.ma')
        m_a = j_p.MorphemeAnalyzer()

        ret = m_a.analyze(string)
        ret = m_a.postProcess(ret)
        ret = m_a.leaveJustBest(ret)

        stl = m_a.divideToSentences(ret)
        result_list = []
        for i in range(stl.size()):
            sentence = stl.get(i)

            morphs_list = []
            for j in range(sentence.size()):
                eoj = sentence.get(j)
                for k in range(eoj.size()):
                    morphs_list.append(eoj.get(k).getString() + '/' + eoj.get(k).getTag())
            result_list.append([sentence.getSentence(), morphs_list])
        return result_list

    def tokens(self, string):
        """형태소 분리

        형태소 분석 후에 분리된 형태소만 얻는 함수 입니다.

        Args:
            string(str): 형태소 분리할 문장

        Returns:
            분리된 형태소의 list

        """
        morphs_list = []
        analyze = self.analyze(string)
        import re

        for i in analyze:
            for j in i[1]:
                morphs_list.append(re.sub("/.+", "", j))

        return morphs_list
