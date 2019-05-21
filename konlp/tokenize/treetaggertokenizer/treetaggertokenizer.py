# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean automatic TreeTagger tokenizer
#
#
# Author: SungHwan Son <zldejagkcm@naver.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""한국어 TreeTagger 토큰화 도구

TreetaggerTokenizer 는 한국어 문장에 대하여 Treetagger를 위한 토큰화를 제공합니다.
기존의 Perl 소스를 파이썬으로 구현한 소스입니다.

Example:
    >>> from konlp.tokenize import TreetaggerTokenizer
    >>> tt = TreetaggerTokenizer()
    >>> tt.tokenize('국민대 "자연어처리 연구실"입니다.')
    ['국민대', '"', '자연어처리', '"', '연구실입니다', '.']
"""

from konlp.tokenize.api import TokenizerI
import re

class TreetaggerTokenizer(TokenizerI):
    """한국어 TreeTagger 토큰화 도구

    #TreetaggerTokenizer 는 한국어 문장에 대하여 Treetagger를 위한 토큰화를 제공합니다.
    기존의 Perl 소스를 파이썬으로 포팅한 소스입니다.

    Example:
        >>> from konlp.tokenize import TreetaggerTokenizer
        >>> tt = TreetaggerTokenizer()
        >>> tt.tokenize('국민대 "자연어처리 연구실"입니다.')
        ['국민대', '"', '자연어처리', '"', '연구실입니다', '.']
    """
    def tokenize(self, string):
        """입력 String값을 토큰화합니다.

        문장을 입력으로 받으며, 받은 문장 토큰화를 진행합니다.

        Args:
            string (str): 문장

        Returns:
            str: 토큰화 된 문장
        """

        p1 = re.compile(r'.*<[^>]+>\s*$')
        p2 = re.compile(r"""([0-9]+(?![.,][0-9]+)?|[A-Za-z]+|[.?!…,\/.:;·ㆍㆍ'|
"|‘|’|“|”|“|\＊|＇|\＿\＿|#$|\%|&()*+<=>@\ \-\[\\\]\^`{}
~°±²¶¼½¿×ß÷ˇ˘˙˚|˝|ΔΦΩαβγδθλμνπφχ
ψω―‘|’|“|”|†‡‥…′″※₁₂₃℃℉ℓ№ΩÅ⅓⅔⅛ Ⅰ\.
|Ⅱ\.|Ⅲ\.|Ⅳ\.|Ⅴ\.|Ⅵ\.|Ⅶ\.|Ⅷ\.|Ⅸ\.|Ⅹ\.|ⅰ\.|ⅱ\.|ⅲ\.|
ⅳ\.|ⅴ\.|ⅵ\.|ⅶ\.|ⅷ\.|ⅸ\.|ⅹ\.|ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅰⅱⅲ
ⅳⅴⅵⅶⅷⅸⅹ←↑→↓↔↗↙⇒⇔∀∃∇∈√∞∠∥∧∨∩∪∫∴∵
∼∽≠≡≥≪≫⊃⊆⊙⌒①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑴⑵⑶⑷
⑸⑹⑺⑻⑼⑽⑾⒜⒝⒞ⓐⓑⓒⓓⓔⓛⓝⓧ─━│┬┼▒■□▣▦▨▲
△▶▷▼▽◀◁◆◇◈○◎●◐◑★☆☎☞♀♂♠♡♣♤♥♧♨♩♪
♬♭➀➌、。〃〈〉《》「」『』【】〓〔〕㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩
㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㎉㎎㎏㎐㎖㎗㎜㎝㎞㎡㎢㎥
㎾㏄㏊＞～∥★■~∼\-])""")

        result = []
        sent = string.replace('\ufeff', '')
        if p1.match(sent.strip()) is not None:
            result.append(sent.strip())
        elif sent != '':
            sent = re.sub(r'[~∼～]', '~', sent)
            sent = re.sub(r'[·ㆍ]', '·', sent)
            sent = re.sub(r"['‘’˙`]", "'", sent)
            sent = re.sub(r'[“”"]', '"', sent)
            m = re.split(p2, sent.strip())
            m = list(filter(None, m))

            index = 0
            for i, token in enumerate(m):
                if i + 1 == len(m):
                    if index >= 1:
                        for num in range(index):
                            m[i - index] += '\n' + m[i - index + num + 1]
                            m[i - index + num + 1] = None
                elif token != ' ':
                    index += 1
                elif token == ' ':
                    if index > 1:
                        for num in range(index - 1):
                            m[i - index] += '\n' + m[i - index + num + 1]
                            m[i - index + num + 1] = None
                        index = 0
                    else:
                        index = 0
            m = list(filter(None.__ne__, m))

            for word in m:
                word = re.sub(r'  ', '', word)
                word = re.sub(r'^ ', '', word)
                word = re.sub(r' $', '', word)
                word = re.sub(r' ', '\n', word)
                if word != '':
                    word = word.split('\n')
                    for w in word:
                        result.append(w)
        return result