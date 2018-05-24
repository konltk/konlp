# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit:
#
#
# Author: HyunYoung Lee <hyun02.engineer@gmail.com>
#         GyuHyeon Nam <ngh3053@gmail.com>
#         Younghun Cho <cyh905@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""Korean Natural Language Toolkit morpheme analyzer interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class KmaI:
    """Korean language morpheme analyzer interface"""

    @abstractmethod
    def analyze(self, string):
        """문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장

        Returns:
            list(list(str)): 형태소 후보군들 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        raise NotImplementedError()

    @abstractmethod
    def morphs(self, string):
        """문장을 입력받아 형태소만 출력합니다.

        Args:
            string (str): 형태소 분석을 할 문장

        Returns:
            list(str): 형태소 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        raise NotImplementedError()

    @abstractmethod
    def nouns(self, string):
        """문장을 입력받아 색인어들을 출력합니다.

        Args:
            string (str): 색인어를 추출할 문장

        Returns:
            list(str): 색인어 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        raise NotImplementedError()



@add_metaclass(ABCMeta)
class ChatI:
    """Chat interface"""

    @abstractmethod
    def analyze(self, line):
        """문장을 입력받아 분석된 형태소/품사 열을 출력합니다.

        Args:
            line (str): 형태소 분석을 할 문장

        Returns:
            list(list(str)): 형태소 분석 결과 리스트

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생

        """
        raise NotImplementedError()


@add_metaclass(ABCMeta)
class IndexerExtractorInterface(object):

    @abstractmethod
    def indexer_extract(self, query, with_symbol_form=False):
        """
        입력 문장에서 색인어 추출을 하는 함수
        Args:
            input_str (str) : 입력 문장
            with_symbol_form (bool) : 색인어의 원형 출력 여부(Default-False)

        Returns:
            List : [색인어 리스트], [색인어와 색인어 원형 리스트]

             '[ "색인어1", "색인어2", ... ]'
            '[ "색인어1 색인어1-원형", "색인어2 색인어2-원형" ]'

        ex) "학교 어디냐?"
        'with_symbol_form - False 인 경우'
        '['학교/NNG', '어디/NP', '이/VCP', '@Q'] , None'
        'with_symbol_form - True 인 경우'
        '['학교/NNG', '어디/NP', '이/VCP', '@Q'],
        ['학교/NNG 학교/NNG', '어디/NP 어디/NP', '이/VCP 이/VCP', '냐/EF+?/SF @Q']'

        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()
