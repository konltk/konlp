# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: NERTagger of kmou
#
# Author: Jae-Hoon Kim <jhoon@kmou.ac.kr>
#         Ho Yoon <4168615@naver.com>
#         Ho-Min Park <homin2006@hanmail.net>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
""" KMOU NERTagger ver 0.8"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re

from nltk.tag.crf import CRFTagger

try:
    import pycrfsuite
except ImportError:
    pass


class NERTagger(CRFTagger):
    """
    python-CRFsuite로 구현한 개체명인식기 모델입니다.

    >>> from konlp.tag import NERTagger
    >>> ner = NERTagger()

    >>> train_data = [[['한','B-PER'], ['용','I-PER'], ['운','I-PER'], [' ', 'O'], ['씨','O'], ['는','O'], [' ', 'O'], ['행','O'], ['복','O'], ['했','O'], ['다','O']]
    ... [['나','O'], ['는','O'], [' ', 'O'], ['서','B-LOC'], ['울','I-LOC'], ['에','O'], [' ', 'O'], ['산','O'],  ['다','O']]]

    >>> ner.train(train_data,'NER.model')
    >>> ner.tag("한용운씨는 사람이다.")
   [('박', 'B-PER'), ('용', 'I-PER'), ('운', 'I-PER'), (' ', 'O'), ('씨', 'O'), ('는', 'O'), (' ', 'O'), ('사', 'O'), ('람', 'O'), ('이', 'O'), ('다', 'O'), ('.', 'O')]

    """

    def __init__(self, feature_func=None, verbose=False, training_opt={}):
        """
        파이썬 CRFTagger를 상속받아 사용합니다.

        Args:
            feature_func: 자질 추출하는 함수입니다. 함수를 넣을 경우에는 인자로 sent인자만 있으면 됩니다. _get_features 함수를 보시면 자세한 정보를 알 수 있습니다.
            verbose(boolean): 학습중에 디버깅 메세지를 출력할 것을 알려주는 인자입니다.
            training_opt(dictionary): 학습옵션을 사전형식으로 받는 인자입니다. 옵션들은 아래와 같습니다.

                Set of possible training options (using LBFGS training algorithm).
                 'feature.minfreq' : The minimum frequency of features.
                 'feature.possible_states' : Force to generate possible state features.
                 'feature.possible_transitions' : Force to generate possible transition features.
                 'c1' : Coefficient for L1 regularization.
                 'c2' : Coefficient for L2 regularization.
                 'max_iterations' : The maximum number of iterations for L-BFGS optimization.
                 'num_memories' : The number of limited memories for approximating the inverse hessian matrix.
                 'epsilon' : Epsilon for testing the convergence of the objective.
                 'period' : The duration of iterations to test the stopping criterion.
                 'delta' : The threshold for the stopping criterion; an L-BFGS iteration stops when the
                            improvement of the log likelihood over the last ${period} iterations is no greater than this threshold.
                 'linesearch' : The line search algorithm used in L-BFGS updates:
                                   { 'MoreThuente': More and Thuente's method,
                                      'Backtracking': Backtracking method with regular Wolfe condition,
                                      'StrongBacktracking': Backtracking method with strong Wolfe condition
                                   }
                 'max_linesearch' :  The maximum number of trials for the line search algorithm.

                """
        self.BOS = ("@BOS@", 'O')
        self.EOS = ("@EOS@", 'O')
        self.SP = "@SP@"
        self.END = "<END>"
        self._model_file = ''
        self._tagger = pycrfsuite.Tagger()
        self.hangul_re = re.compile(r"[ㄱ-ㅣ가-힣]")
        
        if feature_func is None:
            self._feature_func = self._get_features
        else:
            self._feature_func = feature_func

        self._verbose = verbose
        self._training_options = training_opt
        self._pattern = re.compile(r'\d')

    def is_hangul(self, text):
        return self.hangul_re.search(text) is not None
    
    def _get_context(self, sent, i, window_size=2, train=True):
        """윈도우 사이즈만큼 문장의 크기를 늘려줍니다.

        Args:
            sent(list(str,str)): 문장을 나타내는 인자입니다.
            i(int): 문장안에서 단어를 나타내는 인덱스를 나타내는 인자입니다.
            window_size: 한 단어에서 양쪽으로 몇단어씩을 볼 지 선택하는 인자입니다.
            train: 학습모드에서는 단어만 반환하고 학습모드가 아닐때는 단어와 태그 둘 다 가져오는 인자입니다.

        Returns:
            context(list(str)): 각 단어에 대해서 윈도우사이즈만큼 양쪽 단어를 넣은 리스트를 반환합니다.

        """
        copy_sent = [self.BOS] * window_size + sent[:] + [self.EOS] * window_size
        i = i + window_size
        context = copy_sent[i - window_size: i + window_size + 1]
        if train:
            return [w for w, _ in context]
        else:
            return context

    def _make_context_features(self, context):
        """윈도우사이즈만큼 늘려진 리스트에서 자질을 만듭니다.

        Args:
            context(list(str)): 각 단어에 대해서 윈도우사이즈만큼 양쪽 단어를 넣은 리스트를 가진 인자입니다.

        Returns:
            candidates(list(str)): 단어가 들어간 조합이 들어가 있는 리스트를 반환합니다.

        """
        candidates = []
        center = len(context) // 2
        for length in range(1, len(context) + 1):
            for i in range(len(context) - length + 1):
                if length != 1 and not (i <= center < i + length): continue
                candidates.append(("|".join(context[i: i + length]), "w{}-{}".format(i, i + length - 1)))
        return candidates

    def _word2features(self, sent, i, train=True):
        """단어의 자질을 추출하는 함수입니다.

        Args:
            sent(list(str,str)): 문장을 나타내는 인자입니다.
            i(int): 문장안에서 단어를 나타내는 인덱스를 나타내는 인자입니다.

        Returns:
            features(list(str)): 단어의 자질을 포함한 리스트를 반환합니다.

        """
        word = sent[i][0]

        features = [
            'bias',
            'word=' + word,
            'word.isdigit=%s' % word.isdigit(),
            'word.ishangul=%s' % self.is_hangul(word),
        ]
        context = self._get_context(sent, i, train=train)
        context = self._make_context_features(context)
        for w, f in context:
            features.append("{}={}".format(f, w))
        return features

    def _get_features(self, sent, train=True):
        """자질을 추출하는 함수입니다.

        Args:
            sent(list(list(str,str))): 학습데이터에서 들어오는 문장인자입니다.

        Returns:
            features(list(list(str))): 각 단어의 자질을 포함한 리스트입니다.

        """
        return [self._word2features(sent, i, train=train) for i in range(len(sent))]

    def _sent2labels(self, sent):
        """라벨을 반환하는 함수입니다

        Args:
            sent(list(list(str,str))): 학습데이터에서 들어오는 문장인자입니다.

        Returns:
            label(list(list(str))): 각 단어의 자질을 포함한 리스트입니다.

        """
        return [label for token, label in sent]

    def train(self, train_data, model_file):
        """학습해서 CRF모델을 만들어 주는 함수입니다.

        Args:
            train_data(list(list(list(str,str)))): 학습데이터입니다.

        """
        X_train = [self._get_features(s) for s in train_data]
        Y_train = [self._sent2labels(s) for s in train_data]
        trainer = pycrfsuite.Trainer(verbose=self._verbose)
        trainer.set_params(self._training_options)
        for xseq, yseq in zip(X_train, Y_train):
            trainer.append(xseq, yseq)
        trainer.train(model_file)
        self.set_model_file(model_file)

    def set_model_file(self, model_file):
        self._model_file = model_file
        self._tagger.open(self._model_file)

    def _split_bio_tag(self, tag):
        """BI-Tag로 이뤄진 태그를 (B,tag)의 형식으로 바꿔주는 함수입니다.

        Args:
            tag(str): 현재 태그를 인자로 받습니다.

        Returns:
            tuple(str,str): (B,tag)의 형식으로 바꿔서 반환됩니다.

        """
        return (tag, tag) if not re.search('^[BI]', tag) else (tag[0], tag[2:])

    def _is_same_entity(self, prev_tag, curr_tag):
        """전의 라벨과 현재 라벨이 일치한지 보는 함수입니다.

        Args:
            prev_tag(str): 전의 라벨를 인자로 받습니다.
            curr_tag(str): 현재 라벨을 인자로 받습니다.

        Returns:
            (boolean): 같으면 True 다르면 False를 반환합니다.

        """
        if prev_tag == curr_tag:
            return True

        prev_bio, prev_entity = prev_tag
        curr_bio, curr_entity = curr_tag
        if prev_entity == curr_entity and prev_bio == 'B' and curr_bio == 'I':
            return True

        return False

    def _squeeze_entities(self, index, tags):
        """라벨들의 연속된 열에서 O와 BI를 묶어주는 함수입니다.

        Args:
            index(int): 현재 문자의 인덱스를 인자로 받습니다.
            tags(list(str)): CRF모델이 예측한 태그들을 인자로 받습니다.

        Returns:
            squeezed(list(str,int,int)): 태그, 길이, 인덱스를 가지는 리스트를 반환합니다.

        """
        tags = [self._split_bio_tag(t) for t in tags]
        indexed_tags = [[t, 0, index + i] for i, t in enumerate(tags)]
        indexed_tags = indexed_tags + [[(self.END, self.END), 0, index + len(tags)]]

        unified_tags = [indexed_tags[0]]
        for prev, curr in zip(indexed_tags, indexed_tags[1:]):
            if self._is_same_entity(prev[0], curr[0]): continue
            unified_tags.append(curr)

        squeezed = list()
        for curr, after in zip(unified_tags, unified_tags[1:]):
            curr_tag, curr_length, curr_index = curr
            _, _, after_index = after
            squeezed.append([curr_tag[1], after_index - curr_index, curr_index])
        return squeezed

    def tag(self, sent):
        if self._model_file == '':
            raise Exception(' No model file is found !! Please use train or set_model_file function')
        result = []
        syllables = [c if c != ' ' else self.SP for c in sent]
        tags = ['O'] * len(syllables)
        sentence = [(s, t) for s, t in zip(syllables, tags)]
        predicted_tags = self._tagger.tag(self._get_features(sentence))
        for i, tag in enumerate(predicted_tags):
            result.append((sent[i], tag))
        return result

