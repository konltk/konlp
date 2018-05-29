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

현재 KGUNER은 ner, file_ner 기능을 제공합니다.
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
        raise NotImplemented

    def file_ner(self, filename_input, filename_output):
        """
        CONLL 양식의 한국어 단어 및 품사 리스트 파일을 분석하여 결과값을 덧붙여 출력함

        Args:
            filename_input(str) : 입력 파일 경로 (CONLL 양식으로 단어와 품사 정보가 나열되어 있어야 함)
            filename_output(str) : 출력 파일 경로

        """
        with codecs.open(filename_input, encoding="utf-8") as f:
            words, pos = [], []
            for line in f:
                line = line.strip()
                items = line.split("\t")
                if len(items) > 2:
                    words.append(items[0])
                    pos.append(items[1])
                elif words:
                    predictions = self.recognize_entity(words, pos)

                    with codecs.open(filename_output, "a", encoding="utf-8") as w:
                        for word, p, pred in zip(words, pos, predictions):
                            w.write("%s\t%s\t%s\n" % (word, p, pred))
                        w.write("\n")

                    words = []
                    pos = []
