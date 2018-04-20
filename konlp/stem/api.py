# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit:
#
#
# Author: HyunYoung Lee <hyun02.engineer@gmail.com>
#         GyuHyeon Nam <ngh3053@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ============================================================
"""Korean Natural Language Toolkit stemmer interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class StemmerI(object):
    """Stemmer Interface"""

    @abstractmethod
    def stem(self, token):
        """Strip affixes from the token and return the stem.

        Args:
            token (str): The token that should be stemmed.

        Returns:
            str: Stemming token

        Raises:
            NotImplementedError: If not implement this method on a class that extends this class
        """

        raise NotImplementedError()


class SimpleStemmer(StemmerI):
    """For an example about how to use the interface above"""

    def stem(self, token):
        """주격, 목적격 조사를 제거하는 stemmer

        Args:
            token (str): 조사를 제거할 토큰

        Returns:
            str: 조사가 제거된 토큰

        """
        if token[-1] in "은는이가을를":
            return token[:-1]

        else:
            return token
