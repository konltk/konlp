# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit:
#
#
# Author: Seonwu Kim (kimsw@kyonggi.ac.kr)
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ============================================================


"""
KGUNER 한국어 개체명 인식기

이 코드는 Bi-GRU CRF (Char Bi-GRU) 기반의 한국어 개체명 인식기 모델을 wrapping한 코드입니다
2016 국어정보처리 데이터셋을 활용하여 학습하였으며,
경기대학교 ICL(Intelligent Content Lab.)에서 만들어졌습니다.

현재 KGUNER은 ner 기능을 제공합니다.
"""


import codecs
import tensorflow as tf
from konlp.tag.kguner.lib.config import Config
from konlp.tag.kguner.lib.ner_model import NERModel

from konlp.tag.api import TaggerI


class KGUNER(TaggerI):
    def __init__(self):
        self.config = Config()
        self.config.batch_size = 1
        self._load_graph()

    def _load_graph(self):
        # 고정 그래프 로딩
        with tf.gfile.GFile(self.config.dir_model + "freeze.pb", "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            self.model = NERModel(self.config)
            tf.import_graph_def(graph_def, name="prefix")
            self.graph = graph
            self.model.sess = tf.Session(graph=self.graph)

    def ner(self, words, pos):
        """
        Args:
            words(list(str)) : 단어 리스트
            pos(list(str)) : 단어에 대한 품사 리스트

        Returns:
            prediction NER Tags (list(str))
        """
        lex_vecs = self.config.processing_lexicon(words)
        proc_words = [self.config.processing_word(words, i) for i in range(len(words))]
        if type(proc_words[0]) == tuple:
            proc_words = zip(*proc_words)
        proc_pos = [self.config.processing_pos(pos, i) for i in range(len(pos))]

        predict = self.model.predict_batch_in_graph([proc_words], [proc_pos], self.graph,
                                                    lexicon_vecs=[lex_vecs])
        predict = [self.model.idx_to_tag[pred] for pred in predict[0]]

        return predict

    def tag(self, sentence):
        ## 품사 정보가 필요한데 사용할 수 없어, 일단 미구현 상태로 두었습니다.
        raise NotImplemented
