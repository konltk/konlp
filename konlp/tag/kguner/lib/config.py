"""
    2018.02.01
    전반 변수 통제 클래스
"""

# -*- coding:utf-8 -*-

import os
from konlp.tag.kguner.lib.data_utils import *
from konlp.tag.kguner.lib.feature_utils import processing_lexicon, loading_lexicons


class Config():
    def __init__(self, load=True):
        # load if requested (default)
        if load:
            self.load()

    def load(self):

        if self.use_embeddings:
            self.vocab_words, self.embeddings = loading_w2v(self.filename_glove)
        else:
            self.vocab_words = load_vocab(self.filename_words)
            self.embeddings = None

        # 1. vocabulary
        self.vocab_tags = load_vocab(self.filename_tags)
        self.vocab_pos = load_vocab(self.filename_pos)
        self.vocab_chars = load_vocab(self.filename_chars)
        self.nwords = len(self.vocab_words)
        self.nchars = len(self.vocab_chars)
        self.npos = len(self.vocab_pos)
        self.ntags = len(self.vocab_tags)

        # 2. get processing functions that map str -> id
        self.processing_word = get_processing_word(vocab_words=self.vocab_words,
                                                   vocab_chars=self.vocab_chars,
                                                   lowercase=True,
                                                   chars=self.use_chars)
        self.processing_pos = get_processing_word(self.vocab_pos,
                                                  lowercase=False,
                                                  allow_unk=True,
                                                  tag_proc=True)
        self.processing_tag = get_processing_word(self.vocab_tags,
                                                  lowercase=False,
                                                  allow_unk=False,
                                                  tag_proc=True)
        if self.use_lexicons:
            self.lexicon = loading_lexicons(lexicon_dir=self.lexicon_dir)
            self.lexicon_dims = len(self.lexicon)
            self.processing_lexicon = processing_lexicon(lexicon=self.lexicon, vocab_tag=self.vocab_tags, ntype=True)
        else:
            self.processing_lexicon = None

    # embeddings
    dim_word = 100
    dim_char = 30
    dim_pos = 50

    # glove files
    filename_glove = "konlp/tag/kguner/data/kner/mor_word_vec_300_10_50_3_f.vec"
    use_pretrained = True

    # dataset
    data_dir = "konlp/tag/kguner/data/kner/"
    lexicon_dir = data_dir + "lexicons/"

    max_iter = None  # if not None, max number of examples in Dataset

    # vocab (created from dataset with build_data.py)
    filename_words = data_dir + "words.txt"
    filename_tags = data_dir + "tags.txt"
    filename_pos = data_dir + "pos.txt"
    filename_chars = data_dir + "chars.txt"
    dir_model = data_dir + "model.weight/"

    dic_dir = "./dic/"

    # training
    train_embeddings = True
    nepochs = 50
    dropout = 0.8
    batch_size = 20
    lr_method = "adam"
    lr = 0.001
    lr_decay = 0.9
    clip = -1  # if negative, no clipping
    nepoch_no_imprv = 3


    # model hyperparameters
    hidden_size_char = 100  # lstm on chars
    hidden_size_lstm = 300  # lstm on word embeddings

    # NOTE: if both chars and crf, only 1.6x slower on GPU
    use_crf = True  # if crf, training is 1.7x slower on CPU
    use_chars = True  # if char embedding, training is 3.5x slower on CPU
    use_lexicons = True
    use_embeddings = True

    lexicon_type = "ADD"
