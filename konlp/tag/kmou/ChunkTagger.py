# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: ChunkTagger of kmou
#
# Author: Jae-Hoon Kim <jhoon@kmou.ac.kr>
#         Young Namgoong <aei0109@naver.com>
#         Ho Yoon <4168615@naver.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
from nltk.chunk import RegexpParser
from nltk.tree import Tree
import re

from konlp.tag.api import TaggerI


""" Korean Auxiliary Verb Phrase Recognizer ver.0.8"""


class VXP_ChunkTagger(TaggerI):
    """

    >>> ct = VXP_ChunkTagger()

    >>> sent = '가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'

    >>> ct.tag(sent)
    '가게/NNG+에서/JKB 사/VV+아_가지/VXP+고_가/VXP+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'

    """

    def __init__(self):
        self._CHUNK_RULE_VXP_ = "Data\ChunkingRule_VXP.txt"

    def set_chunk_rule(self, rule_file):
        self._CHUNK_RULE_VXP_ = rule_file

    def _make_chunkStruct(self, sent):
        """Transform the input sentence into list of tuples.
        Args:
            sent (str): tagged sentence
            가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC ...

        Returns:
            tuple_sent (list(tuple(str, str))): morphemes in tuple
            [('가게', 'NNG'), ('에서', 'JKB'), ('사', 'VV'), ('아', 'EC'), ('가지', 'VV'), ('고', 'EC'), ('가', 'VV'), ('ㄴ', 'ETM'), ('사탕', 'NNG'), ('이나', 'JC'), ('초콜릿', 'NNG'), ('에', 'JKB'), ('대하', 'VV'), ('어서는', 'EC'), ...]
        """
        tuple_sent = []
        sent = re.split('\+|\s', sent)

        for morph in sent:
            morph = tuple(morph.split('/'))
            tuple_sent.append(morph)

        return tuple_sent

    def _ChunkingRule(self, ChunkingRule):
        """Open Chunking rules in a data text file.

        Args:
            ChunkingRule (str): address of the file which contains chunking rules of an phrase

        Returns:
            ChunkRules (str): string of whole chunking rules of an phrase

        """
        ChunkRules = open(ChunkingRule, 'r').read()

        return ChunkRules

    def _chunker(self, tuple_sent):
        """Chunk base-phrases using chunking rules.

        Args:
            tuple_sent (list(tuple(str, str)))

        Returns:
            chunk_struct Tree('S', [Tree('CHUNK', [(str, str), (str, str)]], (str, str), ...): chunked sentence
        """
        chunkTreeList = []

        chunker = RegexpParser(self._ChunkingRule(self._CHUNK_RULE_VXP_))

        chunk_struct = chunker.parse(tuple_sent)

        return chunk_struct

    def _toStr(self, chunk_struct, sent):
        """Transform chunk tree form into string form which is same with input data format.

        Args:
            chunk_struct (Tree)
            sent (str): POS tagged & spaced sentence

        Returns:
            sent (str): chunked sentence
        """
        for morph in chunk_struct:
            if type(morph) != tuple:
                chunked_morph = morph[0][0]
                for idx in range(1, len(morph)):
                    chunked_morph += '_' + morph[idx][0]
                chunked_morph += '/' + morph.label()

                re_morph = morph[0][0] + '/' + morph[0][1]
                for idx in range(1, len(morph)):
                    re_morph += '.' + morph[idx][0] + '/' + morph[idx][1]

                sent = re.sub(re_morph, chunked_morph, sent)

        return sent

    def tag(self, sent):
        """Chunking phrase and tagging

        Args:
            sent (str): POS tagged & spaced sentence

        Returns:
            _toStr (str): chunked and tagged sentence

        """
        chunk_struct = self._chunker(self._make_chunkStruct(sent))
        return self._toStr(chunk_struct, sent)


""" Korean Particle Equivalent Phrase Recognizer ver.0.8"""


class JSP_ChunkTagger(TaggerI):
    """

    >>> ct = JSP_ChunkTagger()

    >>> sent = '가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'

    >>> ct.tag(sent)
    '가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에_대하_어서는/JSP 별/MM 말/XR+이/JKS 없/VA+었/EP+다/EF+./SF'

    """

    def __init__(self):
        self._CHUNK_RULE_JSP_ = "Data\ChunkingRule_JSP.txt"

    def set_chunk_rule(self, rule_file):
        self._CHUNK_RULE_JSP_ = rule_file

    def _make_chunkStruct(self, sent):
        """Transform the input sentence into list of tuples.
        Args:
            sent (str): tagged sentence
            가게/NNG+에서/JKB 사/VV+아/EC 가지/VV+고/EC 가/VV+ㄴ/ETM 사탕/NNG+이나/JC 초콜릿/NNG+에/JKB 대하/VV+어서는/EC ...

        Returns:
            tuple_sent (list(tuple(str, str))): morphemes in tuple
            [('가게', 'NNG'), ('에서', 'JKB'), ('사', 'VV'), ('아', 'EC'), ('가지', 'VV'), ('고', 'EC'), ('가', 'VV'), ('ㄴ', 'ETM'), ('사탕', 'NNG'), ('이나', 'JC'), ('초콜릿', 'NNG'), ('에', 'JKB'), ('대하', 'VV'), ('어서는', 'EC'), ...]
        """
        tuple_sent = []
        sent = re.split('\+|\s', sent)

        for morph in sent:
            morph = tuple(morph.split('/'))
            tuple_sent.append(morph)

        return tuple_sent

    def _ChunkingRule(self, ChunkingRule):
        """Open Chunking rules in a data text file.

        Args:
            ChunkingRule (str): address of the file which contains chunking rules of an phrase

        Returns:
            ChunkRules (str): string of whole chunking rules of an phrase

        """
        ChunkRules = open(ChunkingRule, 'r').read()

        return ChunkRules

    def _chunker(self, tuple_sent):
        """Chunk base-phrases using chunking rules.

        Args:
            tuple_sent (list(tuple(str, str)))

        Returns:
            chunk_struct Tree('S', [Tree('CHUNK', [(str, str), (str, str)]], (str, str), ...): chunked sentence
        """
        chunkTreeList = []

        chunker = RegexpParser(self._ChunkingRule(self._CHUNK_RULE_JSP_))

        chunk_struct = chunker.parse(tuple_sent)

        return chunk_struct

    def _toStr(self, chunk_struct, sent):
        """Transform chunk tree form into string form which is same with input data format.

        Args:
            chunk_struct (Tree)
            sent (str): POS tagged & spaced sentence

        Returns:
            sent (str): chunked sentence
        """
        for morph in chunk_struct:
            if type(morph) != tuple:
                chunked_morph = morph[0][0]
                for idx in range(1, len(morph)):
                    chunked_morph += '_' + morph[idx][0]
                chunked_morph += '/' + morph.label()

                re_morph = morph[0][0] + '/' + morph[0][1]
                for idx in range(1, len(morph)):
                    re_morph += '.' + morph[idx][0] + '/' + morph[idx][1]

                sent = re.sub(re_morph, chunked_morph, sent)

        return sent

    def tag(self, sent):
        """Chunking phrase and tagging

        Args:
            sent (str): POS tagged & spaced sentence

        Returns:
            _toStr (str): chunked and tagged sentence

        """
        chunk_struct = self._chunker(self._make_chunkStruct(sent))
        return self._toStr(chunk_struct, sent)




