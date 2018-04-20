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
"""Korean Natural Language Toolkit tonkenizer interface"""

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class TokenizerI(object):
    """Tokenizer Interface"""

    @abstractmethod
    def tokenize(self, string):
        """Return a tokenized copy of string.

        Args:
            string (str): String to tokenize

        Returns:
            list(str): Tokenized tokens

        Raises:
            NotImplementedError: If not implement this method on a class that extends this class
        """

        raise NotImplementedError()


class SimpleTokenizer(TokenizerI):
    """For an example about how to inherit the class above"""

    def tokenize(self, string):
        """Simple string tokenizer by white-space character

        Args:
            string (str):  String to tokenize

        Returns:
            str: Tokenized tokens

        """
        return string.split()
