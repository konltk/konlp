# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Klt 형태소 분석기 for Korean Natural Language Toolkit
#
# Author: Geonyeong Kim <uhi7074@gmail.com>
#
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================

import pytest
from konlp.embedding import KnuWord2Vec
import os
import hashlib

DIR_PATH = os.path.join(os.path.dirname(__file__), 'files/')

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
@pytest.fixture
def input_corpus():
    return os.path.join(DIR_PATH, 'test_w2v.txt')

@pytest.fixture
def w2v_instance():
    w2v = KnuWord2Vec()
    return w2v

def test_train(w2v_instance, input_corpus):
    w2v_instance.train(input_corpus, os.path.join(DIR_PATH, 'temp.vocab'), os.path.join(DIR_PATH, 'temp.out'), 'b')
    assert md5(os.path.join(DIR_PATH, 'temp.vocab'))=="8ccf7276bcb8d24bd254d4f78570abd5" and os.path.isfile(os.path.join(DIR_PATH, 'temp.out'))
    os.remove(os.path.join(DIR_PATH, 'temp.vocab'))
    os.remove(os.path.join(DIR_PATH, 'temp.out'))

def test_model_load(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v.emb'), 'b', "utf-8")
    assert len(w2v_instance.embedding_list) != 0

def test_get_vocab(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v.emb'), 'b', "utf-8")
    assert w2v_instance.get_vocab()["UNK"] == 0
    
def test_get_vector(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v.emb'), 'b', "utf-8")
    assert len(w2v_instance.get_vector("UNK")) != 0

def test_get_all_vector(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v.emb'), 'b', "utf-8")
    assert len(w2v_instance.get_all_vector()) != 0 
    
def test_text_train(w2v_instance, input_corpus):
    w2v_instance.train(input_corpus, os.path.join(DIR_PATH, 'temp_text.vocab'), os.path.join(DIR_PATH, 'temp_text.out'), 't')
    assert md5(os.path.join(DIR_PATH, 'temp_text.vocab'))=="8ccf7276bcb8d24bd254d4f78570abd5" and os.path.isfile(os.path.join(DIR_PATH, 'temp_text.out'))
    os.remove(os.path.join(DIR_PATH, 'temp_text.vocab'))
    os.remove(os.path.join(DIR_PATH, 'temp_text.out'))

def test_text_model_load(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v_text.emb'), 't', "utf-8")
    assert len(w2v_instance.embedding_list) != 0

def test_text_get_vocab(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v_text.emb'), 't', "utf-8")
    assert w2v_instance.get_vocab()["UNK"] == 0
    
def test_text_get_vector(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v_text.emb'), 't', "utf-8")
    assert len(w2v_instance.get_vector("UNK")) != 0

def test_text_get_all_vector(w2v_instance, input_corpus):
    w2v_instance.model_load(os.path.join(DIR_PATH, 'test_w2v_text.emb'), 't', "utf-8")
    assert len(w2v_instance.get_all_vector()) != 0 