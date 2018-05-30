# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Korean automatic word spacing
#
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""한국어 자동 띄어쓰기 프로그램 모델

BiLSTMCRF 클래스는 tensorflow로 Bidirectional-LSTM-CRF 모델을 구현하여
한국어 자동 띄어쓰기를 수행하는 클래스입니다.
자동 띄어쓰기를 sequence labeling 문제로 간주하여 문장의 각 음절에
B(어절의 시작부분), I(어절에서 시작을 제외한 나머지 음절) 태그를 부착합니다.

"""

import os
import pickle

import tensorflow as tf
from tensorflow.contrib import rnn


class CharDic:
    """음절 사전

    음절 사전을 가져와서 각 음절에 번호를 부여합니다.
    """
    def __init__(self, file_dir):

        self.UNKNOWN_TAG = 0
        self.word_to_ix = {}

        with open(file_dir, 'rb') as handle:
            self.word_to_ix = pickle.load(handle)

        self.len = len(self.word_to_ix) + 1

    def __len__(self):
        return self.len

    def __getitem__(self, ch):
        if ch in self.word_to_ix:
            return self.word_to_ix[ch]
        else:
            return self.UNKNOWN_TAG


class BiLSTMCRF:
    """한국어 자동 띄어쓰기 프로그램 모델

    BiLSTMCRF 클래스는 tensorflow로 Bidirectional-LSTM-CRF 모델을 구현하여
    한국어 자동 띄어쓰기를 수행하는 클래스입니다.
    자동 띄어쓰기를 sequence labeling 문제로 간주하여 문장의 각 음절에
    B(어절의 시작부분), I(어절에서 시작을 제외한 나머지 음절) 태그를 부착합니다.

    """
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        self.embedding_size = 300
        self.hidden_size = 200
        self.num_classes = 2
        self.num_rnn_layer = 3

        self.model_dir = os.path.join(os.path.dirname(__file__), 'lib/model')
        self.char_dic_dir = os.path.join(os.path.dirname(__file__), 'data/word_dict.pickle')

        self.char_dic = CharDic(self.char_dic_dir)

        self._init_placeholder()
        self._init_variable()
        self._make_graph()

    def _init_placeholder(self):
        # batch, seq
        self.x = tf.placeholder(tf.int32, [None, None])
        self.y = tf.placeholder(tf.int32, [None, None])

        self.len = tf.placeholder(tf.int32, [None])
        self.max_len = tf.placeholder(tf.int32)

        self.batch_size = tf.placeholder(tf.int32, [])

        self._loss = tf.placeholder(tf.float32)
        self._acc = tf.placeholder(tf.float32)

    def _make_bilstm_crf_n_layer(self):
        self.cell_fw = rnn.MultiRNNCell([rnn.LSTMCell(self.hidden_size) for _ in range(self.num_rnn_layer)])
        self.cell_bw = rnn.MultiRNNCell([rnn.LSTMCell(self.hidden_size) for _ in range(self.num_rnn_layer)])
        self.init_state_fw = self.cell_fw.zero_state(self.batch_size, dtype=tf.float32)
        self.init_state_bw = self.cell_bw.zero_state(self.batch_size, dtype=tf.float32)

        self.outputs, state = tf.nn.bidirectional_dynamic_rnn(cell_fw=self.cell_fw,
                                                              cell_bw=self.cell_bw,
                                                              inputs=self.embedding,
                                                              sequence_length=self.len,
                                                              initial_state_fw=self.init_state_fw,
                                                              initial_state_bw=self.init_state_bw,
                                                              dtype=tf.float32)

        self.outputs = tf.concat(self.outputs, 2)
        self.outputs = tf.contrib.layers.fully_connected(inputs=self.outputs,
                                                         num_outputs=self.num_classes,
                                                         activation_fn=None)

        self.log_likelihood, transition_params = tf.contrib.crf.crf_log_likelihood(self.outputs, self.y, self.len)
        self.outputs, viterbi_score = tf.contrib.crf.crf_decode(self.outputs, transition_params, self.len)
        self.loss = tf.reduce_mean(-self.log_likelihood)

    def _init_variable(self):
        self.word_embeddings = tf.get_variable(
            'word_embeddings',
            [len(self.char_dic), self.embedding_size]
        )

    def _make_graph(self):
        self.embedding = tf.nn.embedding_lookup(self.word_embeddings, self.x)

        self._make_bilstm_crf_n_layer()

        self.optimizer = tf.train.AdamOptimizer()
        self.optimize = self.optimizer.minimize(self.loss)


    def _padding(self, lst, value=0):
        lengths = [len(elem) for elem in lst]
        max_length = max(lengths)

        for elem in lst:
            for _ in range(max_length - len(elem)):
                elem.append(value)

        return lst, lengths

    def _char2idx(self, x_data):
        return [[self.char_dic[ch] for ch in sentence] for sentence in x_data]

    def _label2idx(self, y_data):
        return [[1 if l == 'B' else 0 for l in label] for label in y_data]

    def tokenize(self, sents):
        """자동 띄어쓰기 함수

        문장들 리스트를 입력받아 자동 띄어쓰기를 수행합니다.

        Args:
            sents (list): 문장들 리스트

        Returns:
            list: 띄어쓰기가 된 문장들 리스트
        """
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            saver.restore(sess, self.model_dir)

            sents = [sent.replace(' ', '') for sent in sents]
            x_data = self._char2idx(sents)
            x_data, x_len = self._padding(x_data, 0)

            feed_dict = {
                self.x : x_data,
                self.y : [[0] * len(x) for x in x_data],
                self.len : x_len,
                self.max_len : max(x_len),
                self.batch_size : len(sents),
            }

            result = sess.run(self.outputs, feed_dict=feed_dict)

            ret_lst = []
            for origin, pred in zip(sents, result):
                ret_lst.append(''.join(' ' + ch if tag else ch for ch, tag in zip(origin, pred)).strip())
            return ret_lst
