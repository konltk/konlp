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


