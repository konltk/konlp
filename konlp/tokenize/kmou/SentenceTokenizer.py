# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: SentenceTokenizer of kmou
#
# Author: Jae-Hoon Kim <jhoon@kmou.ac.kr>
#         Ho-Min Park <homin2006@hanmail.net>
#         Young Namgoong <aei0109@naver.com>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
""" KMOU SentenceTokenizer ver 1.0"""

from nltk.tag.crf import CRFTagger
from nltk.tag import untag
import re
import konlp

class SentenceTokenizer():
    def __init__(self):
        """
        python-CRFsuite로 구현한 한국어 문장인식 모델입니다.

        >>> from konlp.tag import NERTagger
        >>> cp=SentenceTokenizer()

        >>> paragraph = '아버지가 방에 들어간다. 학교는 잠을 자는 곳이 아니라 공부하는 곳이다.'

        >>> a.sent_tokenizer(paragraph)
       ['아버지가 방에 들어간다.', '학교는 잠을 자는 곳이 아니라 공부하는 곳이다.']
        """
        self.TAG_YES = 'Y'
        self.TAG_NO = 'N'
        self.EOS = '__self.EOS__'
        self.PADDING = '$$'
        self._MODEL_FILE_ = 'sentence_crf.model'
        self.modelpath = konlp.__path__[0] + "/tokenize/kmou/data/" + "sentence_crf.model"
    def feature_detector(self, tokens, index):
        """자질 추출하는 함수입니다.

        Args:
            tokens(list(str)): 공백에 의해 토크나이징 된 토큰들을 나타내는 인자입니다.
            index(int): 토큰안에서 단어를 나타내는 인덱스를 나타내는 인자입니다.

        Returns:
            feature_list(list(str)): 단어에 대한 자질이 들어가 있는 리스트를 반환합니다.

        """
        word0 = re.sub(r'\W*$', '', tokens[index])
        word1 = re.sub(r'\W*$', '', tokens[index + 1]) if index < len(tokens) - 1 else self.EOS

        if re.search(r'[0-9]$', word0):  # Included "," as decimal point
            shape = 'number'
        elif re.search(r'^[a-zA-A]', word0):
            shape = 'english'
        elif re.search(r'^[가-힝]', word0):
            shape = 'hangul'
        elif re.search(r"^\w", word0):
            shape = 'mixedcase'
        else:
            shape = 'other'

        left_1 = word0[-1] if len(word0) > 1 else self.PADDING
        left_2 = word0[-2] if len(word0) > 2 else self.PADDING
        left_3 = word0[-3] if len(word0) > 3 else self.PADDING
        right1 = word1[0] if len(word1) > 1 else self.PADDING
        right2 = word1[1] if len(word1) > 2 else self.PADDING
        right3 = word1[2] if len(word1) > 3 else self.PADDING

        feature_list = []
        feature_list.append('C11_' + left_1)
        feature_list.append('C12_' + left_2)
        feature_list.append('C13_' + left_3)
        feature_list.append('C21_' + left_3 + left_2)
        feature_list.append('C22_' + left_2 + left_1)
        feature_list.append('C31_' + left_3 + left_2 + left_1)

        feature_list.append('R11_' + right1)
        feature_list.append('R12_' + right2)
        feature_list.append('R13_' + right3)
        feature_list.append('R21_' + right1 + right2)
        feature_list.append('R22_' + right2 + right3)
        feature_list.append('R31_' + right1 + right2 + right3)

        feature_list.append('B21_' + left_1 + right1)
        feature_list.append('B31_' + left_2 + left_1 + right1)

        feature_list.append('S1_' + shape)
        return feature_list

    def _to_sentence(self, tagged_sent):
        """태깅된 어절을 문장으로 바꿔주는 함수입니다.

        Args:
            tagged_sent(list(tuple(str,str))): 각 어절과 태그를 알려주는 리스트나타내는 인자입니다.

        Returns:
            sents(list(str)): 각 문장이 담긴 리스트를 반환합니다.

        """

        sents = []
        sent = []
        for word, tag in tagged_sent:
            if tag == self.TAG_YES:
                sent.append(word)
                sents.append(" ".join(sent))
                sent = []
            else:
                sent.append(word)
        else:
            if sent:
                sents.append(" ".join(sent))

        return sents

    def batch_sent_tokenizer(self, paragraphs):
        """단락들을 문장으로 바꿔주는 함수입니다.

        Args:
            paragraphs(list(str)): 단락들이 리스트 인자로 들어옵니다.

        Returns:
            sentences(list(str)): 단락을 문장단위로 잘라서 반환합니다.
        """
        tagger = CRFTagger(feature_func=self.feature_detector)
        tagger.set_model_file(self.modelpath)
        sentences = []
        for paragraph in paragraphs:
            words = re.split('\s', paragraph.strip())
            tagged = tagger.tag(words)
            sentences.append(self._to_sentence(tagged))
        return sentences

    def sent_tokenizer(self, paragraph):
        """단락을 문장으로 바꿔주는 함수입니다.

        Args:
            paragraph(list(str)): 단락이 리스트 인자로 들어옵니다.

        Returns:
            sentences(list(list(str))): 단락을 문장단위로 잘라서 반환합니다.
        """

        tagger = CRFTagger(feature_func=self.feature_detector)
        tagger.set_model_file(self.modelpath)
        words = re.split('\s+', paragraph.strip())
        tagged = tagger.tag(words)
        return self._to_sentence(tagged)

    def demo(self, test_sents):
        tagger = CRFTagger(feature_func=self.feature_detector)
        tagger.set_model_file(self.modelpath)
        for sent in test_sents:
            tagged = tagger.tag(untag(sent))
            for s in self._to_sentence(tagged):
                print(s)
        print(tagger.evaluate(test_sents))

    def pyt_sent_tokenizer(self, paragraph):
        """단락을 문장으로 바꿔주는 함수입니다. 파이테스트용입니다.

        Args:
            paragraph(list(str)): 단락이 리스트 인자로 들어옵니다.

        Returns:
            sentences(list(list(str))): 단락을 문장단위로 잘라서 반환합니다.
        """
        tagger = CRFTagger(feature_func=self.feature_detector)
        tagger.set_model_file(self.modelpath)
        words = re.split('\s+', paragraph.strip())
        tagged = tagger.tag(words)
        return self._to_sentence(tagged)






