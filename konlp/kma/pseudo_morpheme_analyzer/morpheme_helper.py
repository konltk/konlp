"""
강원대학교 한국어 의사 형태소 분석기
"""
import re
import tensorflow as tf
from konlp.kma.pseudo_morpheme_analyzer import config


class MorphemeHelper(object):
    """
        강원대학교 의사형태소 분석기에 사용되는 함수, 자질 사전 및 입출력 단어 사전 호출을 위한 클래스
    """
    def __init__(self):
        """
            hyper parameter, 사전 경로 설정 및 자질, 입출력 단어 사전 불러오기
        """
        tf.app.flags.DEFINE_string("dictionary_file", config.MORPHEME_ANALYSIS_DATA +
                                   "/vocab.txt", "Word2Vec Dictionary File.")
        tf.app.flags.DEFINE_string("target_dictionary_file", config.MORPHEME_ANALYSIS_DATA +
                                   "/mor_vocab.txt", "Target Word2Vec Dictionary File.")
        tf.app.flags.DEFINE_string("mor_bi_dic_file", config.MORPHEME_ANALYSIS_DATA +
                                   "/bi_gramFreqVector.txt",
                                   "sejong corpus bi-syllable frequency vectors")
        tf.app.flags.DEFINE_string("mor_tri_dic_file", config.MORPHEME_ANALYSIS_DATA +
                                   "/tri_gramFreqVector.txt",
                                   "sejong corpus tri-syllable frequency vectors")
        tf.app.flags.DEFINE_string("train_dir", config.MORPHEME_ANALYSIS_MODEL,
                                   "Training directory.")

        tf.app.flags.DEFINE_integer("batch_size", 1, "Size of mini batch.")
        tf.app.flags.DEFINE_integer("embedding_size", 50, "embedding_size")
        tf.app.flags.DEFINE_integer("hidden_size", 128, "hidden_size")
        tf.app.flags.DEFINE_string("cell_mode", "GRU", "cell_mode")
        tf.app.flags.DEFINE_integer("num_epoch", 10, "number of epoch")
        tf.app.flags.DEFINE_float("learning_rate", 0.001, "learning rate")
        tf.app.flags.DEFINE_integer("max_length", 100, "max_input_length")
        tf.app.flags.DEFINE_integer("rate_per_checkpoint", 5, "percent rate per checkpoint.")
        tf.app.flags.DEFINE_integer("epoch_per_checkpoint", 1, "epoch per checkpoint.")
        tf.app.flags.DEFINE_float("dropout", 1.0, "dropout")
        tf.app.flags.DEFINE_integer("num_layers", 1, "num_layers")
        tf.app.flags.DEFINE_integer("z", 1, "z")

        tf.app.flags.FLAGS._parse_flags()
        self.flags = tf.app.flags.FLAGS

        self.split_length = 100

        self.word2idx = {"<PADDING>": 0, "<UNK>": 1}
        self.idx2word = {0: "<PADDING>", 1: "<UNK>"}
        self.decode_word2idx = {"<PADDING>": 0, "<UNK>": 1}
        self.decode_idx2word = {0: "<PADDING>", 1: "<UNK>"}

        self.mor_bi_dic = {}
        self.mor_tri_dic = {}

        # Dictionary Open
        with open(self.flags.dictionary_file, 'r') as file:
            for line in file:
                line = line.strip()
                tokens = line.split()
                idx = len(self.word2idx)
                self.word2idx[tokens[0]] = idx
                self.idx2word[idx] = tokens[0]
        with open(self.flags.target_dictionary_file, 'r') as file:
            for line in file:
                line = line.strip()
                tokens = line.split()
                idx = len(self.decode_word2idx)
                self.decode_word2idx[tokens[0]] = idx
                self.decode_idx2word[idx] = tokens[0]
        with open(self.flags.mor_bi_dic_file, 'r') as mor_bi_syllable_file:
            for line in mor_bi_syllable_file:
                line = line.strip()
                mor_bi_word = line.split("\t")[0]
                mor_bi_freq = line.split('\t')[1].split()
                self.mor_bi_dic[mor_bi_word] = mor_bi_freq
        with open(self.flags.mor_tri_dic_file, 'r') as mor_tri_syllable_file:
            for line in mor_tri_syllable_file:
                line = line.strip()
                mor_tri_word = line.split("\t")[0]
                mor_tri_freq = line.split('\t')[1].split()
                self.mor_tri_dic[mor_tri_word] = mor_tri_freq

    def formatting_data(self, line):
        """문장 단위 형태소 분석용
        Args:
            line(str): 형태소 분석을 위한 입력 문장
        return:
            test_x(str): 입력 문장을 모델의 입력 형식으로 변환한 list
            sequence_length(int): 입력 문장의 길이
        """
        query = line
        query = re.sub("[0-9]", "0", query)
        test_x = []
        for token in query.split():
            if token in self.word2idx:
                test_x.append(self.word2idx[token])
            else:
                test_x.append(self.word2idx["<UNK>"])
        if len(test_x) > self.flags.max_length:
            test_x = test_x[:self.flags.max_length]
        sequence_length = len(test_x)
        if sequence_length > self.flags.max_length:
            sequence_length = self.flags.max_length
        return test_x, sequence_length

    def has_bi_mor_freq_dic(self, word):
        """bi-gram 단어(word)의 빈도수 벡터를 사전에서 찾기 위한 함수
        Args:
            word(str): 빈도수 벡터를 찾을 bi-gram 단어
        return:
            freq_bi_list: bi-gram 단어의 빈도수 list
        """
        freq_bi_list = [0.0 for _ in range(8)]
        if word in self.mor_bi_dic:
            freq_list = self.mor_bi_dic[word]
            sum_of_freq = 0
            for i in freq_list:
                sum_of_freq += int(i)
            for i, _ in enumerate(freq_list):
                freq_bi_list[i] = (float(freq_list[i]) / sum_of_freq)
        return freq_bi_list

    def has_tri_mor_freq_dic(self, word):
        """tri-gram 단어(word)의 빈도수 벡터를 사전에서 찾기 위한 함수
            Args:
                word(str): 빈도수 벡터를 찾을 tri-gram 단어
            return:
                freq_tri_list: tri-gram 단어의 빈도수 list
            """
        freq_tri_list = [0.0 for _ in range(8)]
        if word in self.mor_tri_dic:
            freq_list = self.mor_tri_dic[word]
            sum_of_freq = 0
            for i in freq_list:
                sum_of_freq += int(i)
            for i, _ in enumerate(freq_list):
                freq_tri_list[i] = (float(freq_list[i]) / sum_of_freq)
        return freq_tri_list

    def split_data(self, line):
        """입력 문장의 길이가 SPLIT_LENGTH 보다 길 경우 문장을 분할하는 함수
        Args :
            line(str): 문장의 길이가 100음절이상의 입력 문장
        return:
            split_syllable_list: 최대 문장의 길이가 100음절이 넘지 않는 어절까지의 문장 list
            Example)
                ... 춘천시 강원대학교 ... 라는 문장에서 100번째 음절이 '원'이라면
                [... 춘천시, 강원대학교 ..., ...]와 같이 97번째 음절에서 분할

        """
        line = line.strip()
        split_syllable_list = []
        syllables = line
        while len(syllables.split()) > self.split_length:
            words = syllables.split(' <SP> ')
            syllable_list = []
            for syllable in words:
                syllable_list += syllable.split() + ['<SP>']
            sum_of_syllable = 0
            for i, _ in enumerate(words):
                if sum_of_syllable + len(words[i].split()) < self.split_length:
                    sum_of_syllable += len(words[i].split())+1
                else:
                    left_line = ' '.join(syllable_list[:sum_of_syllable-1] + ["<End>"])
                    right_line = ' '.join(["<Start>"] + syllable_list[sum_of_syllable:-1])
                    syllables = right_line
                    split_syllable_list.append(left_line)
                    if len(syllables.split()) < self.split_length:
                        split_syllable_list.append(right_line)
                    break
        return split_syllable_list

    @staticmethod
    def make_syllables(line):
        """
        Args:
            line(str): 입력 문장
        return:
            syllables(str): 음절 단위의 입력 문장
        """
        syllables = ""
        for s in line:
            if s == " ":
                syllables += "<SP> "
            else:
                syllables += s + " "
        syllables = "<Start> " + syllables + "<End>"
        return syllables
