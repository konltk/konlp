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
"""Korean Natural Language Tooklit chunker interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass

from konlp.parse.api import ParserI


@add_metaclass(ABCMeta)
class ChunkParserI(ParserI):
    """ChunkParser Interface"""

    @abstractmethod
    def parse(self, tokens):
        """
        Return the best chunk structure for the given tokens
        and return a tree.

        :param tokens: The list of (word, tag) tokens to be chunked.
        :type tokens: list(tuple)
        :rtype: Tree
        """
        raise NotImplementedError()
