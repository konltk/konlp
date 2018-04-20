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
"""Korean Natural Language Toolkit tagger interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class TaggerI(object):
    """Tagger Interface"""

    @abstractmethod
    def tag(self, tokens):
        """Attach the appropriate tag in the given token sequence.

        Args:
            tokens (list(str)): Token sequence

        Returns:
            list(tuple(str, str)): The first string is token, the second string is tag

        Raises:
            NotImplementedError: If not implement this method on a class that extends this class
        """

        raise NotImplementedError()
