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
"""Korean Natural Language Toolkit morpheme analysis interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class KmaI:
    """Korean language morpheme analysis interface"""

    @abstractmethod
    def analyze(self, string):
        """
        문장을 입력받아 모든 형태소/품사 후보군들을 출력합니다.

        [description]
        :param string: 형태소 분석을 할 문장
        :type string: str
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    @abstractmethod
    def morphs(self, string):
        """
        문장을 입력받아 형태소만 출력합니다.

        :param string: 형태소 분석을 할 문장
        :type string: str
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    @abstractmethod
    def nouns(self, string):
        """
        문장을 입력받아 색인어들을 출력합니다.

        :param string: 색인어를 추출할 문장
        :type string: str
        :raises: NotImplementedError
        """
        raise NotImplementedError()

