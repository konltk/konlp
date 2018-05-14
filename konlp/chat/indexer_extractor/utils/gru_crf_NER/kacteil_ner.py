import tensorflow as tf

from konlp.chat.indexer_extractor.utils.gru_crf_NER.ner_General.namedEntityRecognition import NER


class KacteilNER(object):
    def __init__(self, model_path):
        self.ner = NER()
        model = tf.train.latest_checkpoint(model_path) #config.NAMED_ENTITY_ROOT+"/model_new"
        graph = tf.Graph()
        with graph.as_default():
            self.sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
            with self.sess.as_default():
                saver = tf.train.import_meta_graph("{}.meta".format(model))
                saver.restore(self.sess, model)

                self.inputs = graph.get_operation_by_name("BidirectionalRNNCRF/placeholder_inputs/inputs").outputs[0]
                self.pl_hasDic = graph.get_operation_by_name("BidirectionalRNNCRF/placeholder_feature_inputs/hasDic").outputs[0]
                self.sequence_length = graph.get_operation_by_name("BidirectionalRNNCRF/placeholder_inputs/Placeholder").outputs[0]
                self.keep_porv = graph.get_operation_by_name("BidirectionalRNNCRF/placeholder_keep_prob/keep_prob").outputs[0]
                matricized_unary_scores = graph.get_operation_by_name("BidirectionalRNNCRF/crf/MatMul").outputs[0]

                self.unary_scores = tf.reshape(matricized_unary_scores,
                                               [1, self.ner.FLAGS.max_length, len(self.ner.decode_idx2word)])
                self.save_transition = graph.get_operation_by_name("BidirectionalRNNCRF/save_transition").outputs[0]

    def predict_step(self, test_x, test_hasDic, sequence_length, keep_prob):
        output_feed = [self.unary_scores, self.save_transition]
        input_feed = {
            self.inputs: test_x,
            self.pl_hasDic: test_hasDic,
            self.sequence_length: sequence_length,
            self.keep_porv:keep_prob}
        tf_unary_scores, transition = self.sess.run(output_feed, feed_dict=input_feed)

        resultList = []
        for tf_unary_scores_, sequence_length_ in zip(tf_unary_scores, sequence_length):
            tf_unary_scores_ = tf_unary_scores_[:sequence_length_]
            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(tf_unary_scores_, transition)
            resultList.append(viterbi_sequence)

        return resultList

    def get_batch(self, batch_data, max_length):
        symbol = {"PAD_ID": 0}

        batch_train_x, batch_train_y, batch_weights = [], [], []

        batch_sequence_length = []

        for idx in range(len(batch_data)):
            x, y, sequence_length = batch_data[idx]
            batch_sequence_length.append(sequence_length)

            x_pad = [symbol["PAD_ID"]] * (max_length - len(x))
            batch_train_x.append(list(x + x_pad))
            y_pad = [symbol["PAD_ID"]] * (max_length - len(y))
            batch_train_y.append(list(y + y_pad))
            weight = list(([1.0] * len(x)) + [0.0] * (max_length - len(x)))
            batch_weights.append(weight)

        return batch_train_x, batch_train_y, batch_weights, batch_sequence_length

    def test_line(self, line):
        nerResultList = []
        inputEumjuls =  self.ner.make_EumjulSet(line)
        splitEumList = []
        if len(inputEumjuls.split('\t')[0].split()) > 100:
            splitEumList =  self.ner.split_data(inputEumjuls)
        else:
            splitEumList.append(inputEumjuls.split('\t')[0])

        for inputEumjul in splitEumList:
            test_x, sequence_length =  self.ner.formatting_data(inputEumjul)
            test_x, _, _, sequence_length = self.get_batch([(test_x, [], sequence_length)],  self.ner.FLAGS.max_length)
            test_hasDic = []
            for col in range(len(test_x)):
                temp = []
                for row in range(len(test_x[col])):
                    temp.append(0.0)
                test_hasDic.append(temp)
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    dicFeature = [0.0 for _ in range(500)]
                    if  self.ner.idx2word[test_x[j][i]] != '<Start>' and  self.ner.idx2word[test_x[j][i]] != '<End>':
                        if test_x[j][i] != 0:
                            prevEumjul =  self.ner.idx2word[test_x[j][i - 1]]
                            currEumjul =  self.ner.idx2word[test_x[j][i]]
                            nextEumjul =  self.ner.idx2word[test_x[j][i + 1]]
                            dicFeature =  self.ner.hasBiDic(currEumjul + nextEumjul, dicFeature)
                            dicFeature =  self.ner.hasBiDic(prevEumjul + currEumjul, dicFeature)
                    test_hasDic[j][i] = dicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    dicFeature = [0.0 for _ in range(500)]
                    if  self.ner.idx2word[test_x[j][i]] != '<Start>' and  self.ner.idx2word[test_x[j][i]] != '<End>':
                        if len(test_x[j]) >= 5:
                            if test_x[j][i] != 0:
                                middleTriEumjul =  self.ner.idx2word[test_x[j][i - 1]] +  self.ner.idx2word[test_x[j][i]] + \
                                                   self.ner.idx2word[
                                                      test_x[j][i + 1]]
                                if i < 2:
                                    rightTriEumjul =  self.ner.idx2word[test_x[j][i]] +  self.ner.idx2word[test_x[j][i + 1]] + \
                                                      self.ner.idx2word[
                                                         test_x[j][i + 2]]
                                    dicFeature =  self.ner.hasTriDic(middleTriEumjul, dicFeature)
                                    dicFeature =  self.ner.hasTriDic(rightTriEumjul, dicFeature)
                                elif i > len(test_x[j]) - 3:
                                    leftTriEumjul =  self.ner.idx2word[test_x[j][i - 2]] +  self.ner.idx2word[test_x[j][i - 1]] + \
                                                     self.ner.idx2word[
                                                        test_x[j][i]]
                                    dicFeature =  self.ner.hasTriDic(leftTriEumjul, dicFeature)
                                    dicFeature =  self.ner.hasTriDic(middleTriEumjul, dicFeature)

                                else:
                                    leftTriEumjul =  self.ner.idx2word[test_x[j][i - 2]] +  self.ner.idx2word[test_x[j][i - 1]] + \
                                                     self.ner.idx2word[
                                                        test_x[j][i]]
                                    rightTriEumjul =  self.ner.idx2word[test_x[j][i]] +  self.ner.idx2word[test_x[j][i + 1]] + \
                                                      self.ner.idx2word[
                                                         test_x[j][i + 2]]
                                    dicFeature =  self.ner.hasTriDic(leftTriEumjul, dicFeature)
                                    dicFeature =  self.ner.hasTriDic(middleTriEumjul, dicFeature)
                                    dicFeature =  self.ner.hasTriDic(rightTriEumjul, dicFeature)
                    test_hasDic[j][i] += dicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    morDicFeature = []
                    if  self.ner.idx2word[test_x[j][i]] != '<Start>' and  self.ner.idx2word[test_x[j][i]] != '<End>':
                        if test_x[j][i] != 0:
                            prevEumjul =  self.ner.idx2word[test_x[j][i - 1]]
                            currEumjul =  self.ner.idx2word[test_x[j][i]]
                            nextEumjul =  self.ner.idx2word[test_x[j][i + 1]]
                            morDicFeature =  self.ner.hasBiMorFreqDic(prevEumjul + currEumjul)
                            morDicFeature +=  self.ner.hasBiMorFreqDic(currEumjul + nextEumjul)
                    if not morDicFeature:
                        morDicFeature = [0.0 for _ in range(16)]
                    test_hasDic[j][i] += morDicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    morDicFeature = []
                    if  self.ner.idx2word[test_x[j][i]] != '<Start>' and  self.ner.idx2word[test_x[j][i]] != '<End>':
                        if len(test_x[j]) >= 5:
                            if test_x[j][i] != 0:
                                middleTriEumjul =  self.ner.idx2word[test_x[j][i - 1]] +  self.ner.idx2word[test_x[j][i]] + \
                                                   self.ner.idx2word[
                                                      test_x[j][i + 1]]
                                if i < 2:
                                    rightTriEumjul =  self.ner.idx2word[test_x[j][i]] +  self.ner.idx2word[test_x[j][i + 1]] + \
                                                      self.ner.idx2word[
                                                         test_x[j][i + 2]]
                                    leftTriVector = [0.0 for _ in range(8)]
                                    morDicFeature = leftTriVector
                                    morDicFeature +=  self.ner.hasTriMorFreqDic(middleTriEumjul)
                                    morDicFeature +=  self.ner.hasTriMorFreqDic(rightTriEumjul)
                                elif i > len(test_x[j]) - 3:
                                    leftTriEumjul =  self.ner.idx2word[test_x[j][i - 2]] +  self.ner.idx2word[test_x[j][i - 1]] + \
                                                     self.ner.idx2word[
                                                        test_x[j][i]]
                                    morDicFeature =  self.ner.hasTriMorFreqDic(leftTriEumjul)
                                    morDicFeature +=  self.ner.hasTriMorFreqDic(middleTriEumjul)
                                    leftTriVector = [0.0 for _ in range(8)]
                                    morDicFeature += leftTriVector

                                else:
                                    leftTriEumjul =  self.ner.idx2word[test_x[j][i - 2]] +  self.ner.idx2word[test_x[j][i - 1]] + \
                                                     self.ner.idx2word[
                                                        test_x[j][i]]
                                    rightTriEumjul =  self.ner.idx2word[test_x[j][i]] +  self.ner.idx2word[test_x[j][i + 1]] + \
                                                      self.ner.idx2word[
                                                         test_x[j][i + 2]]
                                    morDicFeature =  self.ner.hasTriMorFreqDic(leftTriEumjul)
                                    morDicFeature +=  self.ner.hasTriMorFreqDic(middleTriEumjul)
                                    morDicFeature +=  self.ner.hasTriMorFreqDic(rightTriEumjul)
                    if not morDicFeature:
                        morDicFeature = [0.0 for _ in range(24)]
                    test_hasDic[j][i] += morDicFeature
            predict = self.predict_step(test_x, test_hasDic, sequence_length, self.ner.FLAGS.dropout)
            #                 print predict
            strResult = ""
            for s in predict[0]:
                strResult +=  self.ner.decode_idx2word[s] + " "
            print_result_set =  self.ner.restore(inputEumjul, strResult)
            nerResult = ""
            for i in print_result_set:
                nerResult += i + " "

            nerResultList.append(nerResult)
        return nerResultList
