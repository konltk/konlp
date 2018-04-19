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
        """
        Strip affixes from the token and return the stem.

        :param token: The token that should be stemmed.
        :type token: str
        """
        raise NotImplementedError()


class SimpleStemmer(StemmerI):
    """for an example about how to use the interface above"""

    def stem(self, token):
        if token[-1] in "은는이가을를":
            return token[:-1]
        else:
            return token
