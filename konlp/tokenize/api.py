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
        """
        Return a tokenized copy of string.

        :param string: string to tokenize
        :type string: str
        :raises: NotImplementedError
        """
        raise NotImplementedError()


class SimpleTokenizer(TokenizerI):
    """For an example about how to inherit the class above"""

    def tokenize(self, string):
        return string.split()
