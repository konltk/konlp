import codecs
import numpy as np
import os
import re
from konlp.tag.kguner.lib.data_utils import MyIOError


def loading_lexicon(filename, lexicon):
    try:
        with codecs.open(filename, encoding='utf-8') as f:
            lexicon_type = filename[filename.rfind("/")+1:filename.rfind(".")]
            lexicon[lexicon_type] = [entity.strip() for entity in f]
    except IOError:
        raise MyIOError(filename)


def loading_lexicons(lexicon_dir):
    lexicon = {}
    for filename in os.listdir(lexicon_dir):
        filename = os.path.join(lexicon_dir, filename)
        loading_lexicon(filename, lexicon)

    return lexicon


def processing_term(term):
    """
    개체명 정보 및 문장 데이터 정보에 대한 전처리
    :param term: 단어 정보(Str)
    :return: 정규화 처리 된 단어 정보(Str)
    """

    if len(re.findall("[A-Z]", term)) > 1:
        return term.upper()
    return term.lower()


def labeling_indices(entity_in_sentence, label_dict):
    """
    One-hot 인덱스 리스트를 기준으로 Label에 해당하는 인덱싱 제공
    :param entity_in_sentence: 문장에 대한 레이블 태깅 리스트(list)
    :param label_dict: 태그 인덱스 사전(dict)
    :return: label indices(list)
    """

    return [indexing(label, label_dict) for label in entity_in_sentence]


def matching_label_list(label_list, entity_in_sentence):
    """
    전체 레이블 리스트와 개체의 문장 내 정보를 비교하여 적용함
    :param label_list: 전체 레이블 리스트(list)
    :param entity_in_sentence: 개체의 문장 내 레이블 리스트(str)
    :return: 적용된 전체 레이블 리스트(list)
    """

    for i, (label, term) in enumerate(zip(label_list, entity_in_sentence)):
        if label != term:
            if "_" in label:
                continue
            else:
                label_list[i] = term

    return label_list


def tagging_lexicon(words, lexicon, label_dict, type="Protein"):
    """
    개체명 사전을 기반으로 한 단어 태깅
    :param words: 문장 정보(str)
    :param lexicon: 개체명 사전(set)
    :param label_dict: 태그 인덱스 사전(dict)
    :param type: 개체명 사전이 다루는 타입(str)
    :return: One-hot 벡터 구성이 가능한 인덱스 리스트
    """

    # words = [processing_term(word) for word in words]
    label_list = ['O' for _ in words]

    for entity in lexicon:
        if ' ' in entity:
            entitys = entity.split()
            entity = ""
            for ent_term in entitys:
                entity += ((ent_term) + " ")
            entity = entity[:-1]
        else:
            entity = (entity)

        entity_in_sentence = indexing_entity(words, entity, type)
        if entity_in_sentence:
            label_list = matching_label_list(label_list, entity_in_sentence)

    return labeling_indices(label_list, label_dict)


def indexing_entity(words, entity, type="Protein"):
    """
    문장 내 개체명의 정보를 파악하여 태깅
    :param words: 문장의 단어 리스트(list)
    :param entity: 개체명 정보(str)
    :param type: 개체명 사전이 다루는 타입(str)
    :return: onehot 형태의 인덱스 리스트(list)
    """

    index = 0
    entity_index = 0
    entity_terms = entity.split()
    entity_in_sentence = ['O' for _ in words]

    for word in words:
        try:
            if word == entity_terms[entity_index]:
                entity_index += 1
                if entity_index == len(entity_terms):
                    for i in range(entity_index):
                        if (i + 1) == entity_index:
                            entity_in_sentence[index - i] = ("B_" + type)
                        else:
                            entity_in_sentence[index - i] = ("I_" + type)
                    entity_index = 0
            else:
                entity_index = 0
        except Exception:
            print('a')
        index += 1

    if ("B_" + type) in entity_in_sentence:
        return entity_in_sentence
    return None


def indexing(item, dictionary):
    """
    사전에 기반한 인덱싱
    :param item: 인덱싱 대상(str)
    :param dictionary: 인덱스 사전
    :return:
    """

    if item in dictionary:
        if int(dictionary[item]) == 1:
            return -1
        return int(dictionary[item])
    return -1


def onehot(index, nb_labels):
    """
    인덱스의 Onehot 벡터화
    :param index: 인덱스(int)
    :param nb_labels: 전체 레이블 수(int)
    :return: 해당 인덱스의 onehot vec(list)
    """

    vecs = np.zeros(nb_labels, )
    if index == -1:
        return vecs
    vecs[index] = 1
    return vecs


def constructing_lexicon_onehot(sentence, lexicon, label_dict, types):
    """
    onehot 벡터로 구성하는 최종 메소드
    :param words: 문장 정보(str)
    :param lexicon: 개체명 사전(set)
    :param label_dict: 태그 인덱스 사전(dict)
    :param type: 개체명 사전이 다루는 타입(str)
    :return: One-hot 벡터
    """

    return [onehot(index, len(label_dict)) for index in tagging_lexicon(sentence, lexicon, label_dict, types)]


def merged_onehots(sentence, lexicons, label_dict):
    """
    :param sentence: 문장 정보
    :param lexicons: 개체명 사전의 리스트
    :param label_dict: 예측 태그 사전
    :return: 문장 정보에 대한 각 개체명 정보가 One-hot형태로 구성된 벡터
    """

    p_oh = constructing_lexicon_onehot(sentence, lexicons['DT'], label_dict, 'DT')
    d_oh = constructing_lexicon_onehot(sentence, lexicons['LC'], label_dict, 'LC')
    r_oh = constructing_lexicon_onehot(sentence, lexicons['OG'], label_dict, 'OG')
    c_oh = constructing_lexicon_onehot(sentence, lexicons['TI'], label_dict, 'TI')
    s_oh = constructing_lexicon_onehot(sentence, lexicons['PS'], label_dict, 'PS')


    onehot_vec = []
    for p, d, r, c, s in zip(p_oh, d_oh, r_oh, c_oh, s_oh):
        onehot = []
        for po, do, ro, co, so in zip(p, d, r, c, s):
            onehot.append(max([po, do, ro, co, so]))
        onehot_vec.append(onehot)

    return onehot_vec


def processing_lexicon(lexicon, vocab_tag, ntype=True):
    def f(sentence):
        if ntype:
            return tuple(merged_onehots(sentence, lexicon, vocab_tag))
        else:
            return tuple(constructing_lexicon_onehot(sentence, lexicon["Protein"], vocab_tag, "Protein"))
    return f
