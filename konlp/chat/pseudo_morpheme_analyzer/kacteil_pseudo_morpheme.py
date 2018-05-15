"""
강원대학교 한국어 의사 형태소 분석기
"""
import tensorflow as tf
from konlp.chat.pseudo_morpheme_analyzer.morpheme_helper import MorphemeHelper
from konlp.chat.pseudo_morpheme_analyzer.post_processing.restore_morpheme import RestoredMorpheme
from konlp.chat.pseudo_morpheme_analyzer import config


class PseudoMorphemeAnalyzer(object):
    """
    강원대학교 한국어 의사 형태소 분석기
    """
    def __init__(self, model_path):
        """
        의사 형태소 분석기 모델 호출 및 의사 형태소 분석결과를 형태소 분석 결과로 복원 모듈 호출

        Args:
        model_path(str): 의사 형태소 분석기 모델 경로
        """
        self.restore_morpheme = RestoredMorpheme()
        pre_analyzed_dic_path = config.MORPHEME_ANALYSIS_DATA + "pre-analyzedDic.txt"
        self.pre_analyzed_dic = self.restore_morpheme.open_pre_analyzed_dic(pre_analyzed_dic_path)
        restored_dic_path = config.MORPHEME_ANALYSIS_DATA + "DicForRestoration_add.txt"
        self.restore_dic = self.restore_morpheme.open_restore_dic(restored_dic_path)

        self.morpheme_helper = MorphemeHelper()
        model = tf.train.latest_checkpoint(model_path)
        graph = tf.Graph()
        with graph.as_default():
            self.sess = tf.Session(config=
                                   tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
            with self.sess.as_default():
                saver = tf.train.import_meta_graph("{}.meta".format(model))
                saver.restore(self.sess, model)

                self.inputs = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                          "placeholder_inputs/inputs").outputs[0]
                self.pl_has_dic = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                              "placeholder_feature_inputs/"
                                                              "hasDic").outputs[0]
                self.sequence_length = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                                   "placeholder_inputs/"
                                                                   "Placeholder").outputs[0]
                self.keep_prob = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                             "placeholder_keep_prob/"
                                                             "keep_prob").outputs[0]
                matricized_unary_scores = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                                      "crf/MatMul").outputs[0]

                self.unary_scores = tf.reshape(matricized_unary_scores,
                                               [1, self.morpheme_helper.flags.max_length,
                                                len(self.morpheme_helper.decode_idx2word)])
                self.save_transition = graph.get_operation_by_name("BidirectionalRNNCRF/"
                                                                   "save_transition").outputs[0]

    def __predict_step(self, test_x, test_has_dic, sequence_length, keep_prob):
        """의사 형태소 분석기 모델의 predict 함수
        Args:
            test_x: 모델의 입력 list
            test_has_dic: 입력 자질 list
            sequence_length(int): 입력 문자열의 길이
            keep_prob(float): keep_prob

        return:
            result_list: 음절 단위 형태소 분석 결과
        """
        output_feed = [self.unary_scores, self.save_transition]
        input_feed = {
            self.inputs: test_x,
            self.pl_has_dic: test_has_dic,
            self.sequence_length: sequence_length,
            self.keep_prob: keep_prob}
        tf_unary_scores, transition = self.sess.run(output_feed, feed_dict=input_feed)

        result_list = []
        for tf_unary_scores_, sequence_length_ in zip(tf_unary_scores, sequence_length):
            tf_unary_scores_ = tf_unary_scores_[:sequence_length_]
            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores_, transition)
            result_list.append(viterbi_sequence)

        return result_list

    @staticmethod
    def __get_batch(batch_data, max_length):
        """입력 문장 길이 이상의 입력에 max_length 까지 PADDING 추가 함수
        Args:
            batch_data: 모델의 입력 list
            max_length(int): 입력 길이
        return:
            batch_train_x: 모델의 최종 입력 형식 list
            batch_sequence_length: 입력의 길이
        """
        symbol = {"PAD_ID": 0}

        batch_train_x = []

        batch_sequence_length = []
        for idx, _ in enumerate(batch_data):
            _x, sequence_length = batch_data[idx]
            batch_sequence_length.append(sequence_length)

            x_pad = [symbol["PAD_ID"]] * (max_length - len(_x))
            batch_train_x.append(list(_x + x_pad))

        return batch_train_x, batch_sequence_length

    def analyze(self, line):
        """입력에 대한 형태소 분석 함수
        Args:
            line(str): 입력 문장
        return:
            morpheme_results: 형태소 분석 결과 list
        """
        input_syllables = self.morpheme_helper.make_syllables(line)
        split_syllable_list = []
        morpheme_results = []
        if len(input_syllables.split('\t')[0].split()) > self.morpheme_helper.split_length:
            split_syllable_list = self.morpheme_helper.split_data(input_syllables)
        else:
            split_syllable_list.append(input_syllables.split('\t')[0])
        for input_syllable in split_syllable_list:
            test_x, sequence_length = self.morpheme_helper.formatting_data(input_syllable)
            test_x, sequence_length = self.__get_batch([(test_x, sequence_length)],
                                                       self.morpheme_helper.flags.max_length)
            test_has_dic = []
            for col, _ in enumerate(test_x):
                temp = [0.0 for _ in range(len(test_x[col]))]
                test_has_dic.append(temp)
            for j, _ in enumerate(test_x):
                for i in range(len(test_x[j])):
                    morpheme_dic_feature = []
                    if self.morpheme_helper.idx2word[test_x[j][i]] != '<Start>' \
                            and self.morpheme_helper.idx2word[test_x[j][i]]\
                            != '<End>':
                        if test_x[j][i] != 0:
                            prev_syllable = self.morpheme_helper.idx2word[test_x[j][i - 1]]
                            curr_syllable = self.morpheme_helper.idx2word[test_x[j][i]]
                            next_syllable = self.morpheme_helper.idx2word[test_x[j][i + 1]]
                            morpheme_dic_feature = self.morpheme_helper.\
                                has_bi_mor_freq_dic(prev_syllable + curr_syllable)
                            morpheme_dic_feature += self.morpheme_helper.\
                                has_bi_mor_freq_dic(curr_syllable + next_syllable)
                    if not morpheme_dic_feature:
                        morpheme_dic_feature = [0.0 for _ in range(16)]
                    test_has_dic[j][i] = morpheme_dic_feature
            for j, _ in enumerate(test_x):
                for i in range(len(test_x[j])):
                    morpheme_dic_feature = []
                    if self.morpheme_helper.idx2word[test_x[j][i]] != '<Start>' \
                            and self.morpheme_helper.idx2word[test_x[j][i]] != '<End>':
                        if len(test_x[j]) >= 5:
                            if test_x[j][i] != 0:
                                middle_tri_syllable\
                                    = self.morpheme_helper.idx2word[test_x[j][i - 1]]\
                                      + self.morpheme_helper.idx2word[test_x[j][i]]\
                                      + self.morpheme_helper.idx2word[test_x[j][i + 1]]
                                if i < 2:
                                    right_tri_syllable\
                                        = self.morpheme_helper.idx2word[test_x[j][i]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i + 1]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i + 2]]
                                    left_tri_vector = [0.0 for _ in range(8)]
                                    morpheme_dic_feature = left_tri_vector
                                    morpheme_dic_feature += self.morpheme_helper.\
                                        has_tri_mor_freq_dic(middle_tri_syllable)
                                    morpheme_dic_feature += self.morpheme_helper.\
                                        has_tri_mor_freq_dic(right_tri_syllable)
                                elif i > len(test_x[j]) - 3:
                                    left_tri_syllable\
                                        = self.morpheme_helper.idx2word[test_x[j][i - 2]]\
                                            + self.morpheme_helper.idx2word[test_x[j][i - 1]]\
                                            + self.morpheme_helper.idx2word[test_x[j][i]]
                                    morpheme_dic_feature = self.morpheme_helper.\
                                        has_tri_mor_freq_dic(left_tri_syllable)
                                    morpheme_dic_feature += self.morpheme_helper.\
                                        has_tri_mor_freq_dic(middle_tri_syllable)
                                    left_tri_vector = [0.0 for _ in range(8)]
                                    morpheme_dic_feature += left_tri_vector

                                else:
                                    left_tri_syllable\
                                        = self.morpheme_helper.idx2word[test_x[j][i - 2]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i - 1]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i]]
                                    right_tri_syllable\
                                        = self.morpheme_helper.idx2word[test_x[j][i]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i + 1]]\
                                          + self.morpheme_helper.idx2word[test_x[j][i + 2]]
                                    morpheme_dic_feature = self.morpheme_helper.\
                                        has_tri_mor_freq_dic(left_tri_syllable)
                                    morpheme_dic_feature += self.morpheme_helper.\
                                        has_tri_mor_freq_dic(middle_tri_syllable)
                                    morpheme_dic_feature += self.morpheme_helper.\
                                        has_tri_mor_freq_dic(right_tri_syllable)
                    if not morpheme_dic_feature:
                        morpheme_dic_feature = [0.0 for _ in range(24)]
                    test_has_dic[j][i] += morpheme_dic_feature

            predict = self.__predict_step(test_x, test_has_dic, sequence_length,
                                          self.morpheme_helper.flags.dropout)
            str_result = ""
            for _s in predict[0]:
                str_result += self.morpheme_helper.decode_idx2word[_s] + " "
            morpheme_results += self.restore_morpheme.restore_morpheme(input_syllable,
                                                                       str_result,
                                                                       self.restore_dic,
                                                                       self.pre_analyzed_dic)
        return morpheme_results
