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

# import jpype
import sys
import konlp
import platform
# if platform.system() == 'Windows':
#     sys.path = [konlp.__path__[0] + '/lib_win'] + sys.path
import jpype
import json
import os
import sys
import re

# from konlp.kma.api import KmaI
# print(jpype.__version__)

class klt2000:
    def __init__(self, classpath_=False, jvmpath=None):
        """Klt module's __init__ method

        Args:
            dic_path(str): 사전 위치

        """
        import konlp

        # path = os.path.dirname(os.path.abspath(__file__))
        classpath = os.pathsep.join([konlp.__path__[0] + "/kma/kkma/lib/" + "kkma-2.0.jar",konlp.__path__[0] + "/kma/klt2000/lib/" + "klt2000.jar"])
        # print(classpath_)
        jvmpath = jvmpath or jpype.getDefaultJVMPath()
        if jvmpath and not jpype.isJVMStarted():
            if jvmpath and not jpype.isJVMStarted():
                if not classpath_:#classpath_ == None:
                    jpype.startJVM(
                        jvmpath,
                        "-Djava.class.path={classpath}".format(classpath=classpath),
                '-Dfile.encoding=UTF8',
                        '-ea', '-Xmx1024m'
                        # ,convertStrings=True
                    )
                else:
                    cp = self.set_classpath()
                    jpype.startJVM(
                        jvmpath,
                        "-Djava.class.path={classpath}".format(classpath=cp),
                '-Dfile.encoding=UTF8',
                        '-ea', '-Xmx1024m'
                        # ,convertStrings=True
                    )            
        jpkg = jpype.JPackage("HamPack.Run")
        # print(os.sep.join([konlp.__path__[0],"kma","klt2000","hdic"])+os.sep)
        self.kma = jpkg.Morphs(os.sep.join([konlp.__path__[0],"kma","klt2000","hdic"])+os.sep)
        
        self.open_paran = r'\(\【\['
        self.close_paran = r'\)\】\]'
        self.hangul = r'가-힣|a-z|A-Z'
        self.number = r'[0-9]+'

        self.EF_SF_pattern = re.compile(r'([{}]|{})[\s]*([.?!])'.format(self.hangul,self.number))
        # self.EF_SF_pattern = re.compile(r'([{}])[\s]*([.?!])'.format(self.hangul))

    def pos(self, string,sep=''):
        """문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장
            sep (str): 형태소 품사 구분자 (default='/')

        Returns:
            list(list(str)): 형태소 후보군들 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        result = None
        if sep == '':
            result = list(self.kma.pos(string,'/'))
        else:
            result = list(self.kma.pos(string,sep))
        
        #return result#
        return self.to_str(result)

    def morphs(self, string):
        """문장을 입력받아 형태소만 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장

        Returns:
            list(str): 형태소 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """

        result = list(self.kma.morphs(string))

        #return result#
        return self.to_str(result)

    def nouns(self, string):
        """문장을 입력받아 색인어들을 출력합니다.

        Args:
            string (str): 색인어를 추출할 문장

        Returns:
            list(str): 색인어 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        result = list(self.kma.nouns(string))

        #return result#
        return self.to_str(result)

    def options(self,options):
        """token추출시 형태소 분석 옵션을 설정할수 있습니다.

        Args:
            options (dictionary): 설정할 옵션들의 Dictionary, key : str, value : bool
            
        """
        self.kma.setOption(options)
    
    def sent_tokenize(self,text):
        find_pos = 0
        start = 0
        sent_list = []
        dot_count = 0
        while True:
            match = self.EF_SF_pattern.search(text, find_pos)
            if not match: break
            find_pos = match.end()
            sent = text[start:find_pos].strip()
            
            if sent.count('\"') % 2 == 1:
                continue
            elif sent.count("\'") % 2 == 1:
                continue
            elif len(text) != find_pos and text[find_pos:][0] >= '0' and  text[find_pos:][0] <= '9':
                dot_count += 1
                if dot_count == 1:
                    continue
                elif dot_count >= 2:
                    start = find_pos
                    sent_list.append(sent)
                    dot_count = 0
            else:
                start = find_pos
                sent_list.append(sent)
                dot_count = 0
        
        if start < len(text) -1:
            sent = text[start:].strip()
            sent_list.append(sent)

        return sent_list

    def to_str(self,result):
        temp = []
        for re in result:
            temp.append(str(re))
        
        return temp
    
    def set_classpath(self):
        #sys.path = sys.path
        import konlpy
        #print(jpype.__version__)
        folder_suffix = [
            # JAR
            '{0}',
            # Java sources
            '{0}{1}bin',
            '{0}{1}*',
            # Hannanum
            '{0}{1}jhannanum-0.8.4.jar',
            # Kkma
            '{0}{1}kkma-2.0.jar',
            # Komoran3
            '{0}{1}aho-corasick.jar',
            '{0}{1}shineware-common-1.0.jar',
            '{0}{1}shineware-ds-1.0.jar',
            '{0}{1}komoran-3.0.jar',
            # Twitter (Okt)
            '{0}{1}snakeyaml-1.12.jar',
            '{0}{1}scala-library-2.12.3.jar',
            '{0}{1}open-korean-text-2.1.0.jar',
            '{0}{1}twitter-text-1.14.7.jar',
            '{0}{1}*'
        ]

        install_path = konlpy.__path__[0] + os.sep + 'java'
        args = [install_path,os.sep]
        classpath = os.pathsep.join(f.format(*args) for f in folder_suffix)

        classpath_ = [f.format(*args) for f in folder_suffix]

        # for i in classpath_:
        #     jpype.addClassPath(i)

        classpath2 = os.sep.join([konlp.__path__[0],"kma","klt2000","lib","klt2000.jar"])
        #print(classpath2)
        # jpype.addClassPath(classpath2)
        # os.environ['CLASSPATH'] = 
        return os.pathsep.join([classpath,classpath2])
