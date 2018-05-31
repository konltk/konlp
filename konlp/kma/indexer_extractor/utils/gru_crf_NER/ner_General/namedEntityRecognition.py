import re
import tensorflow as tf
from konlp.kma.indexer_extractor.utils.gru_crf_NER.ner_General import gru_crf
from konlp.kma.indexer_extractor import config


class NER(object):
    def __init__(self):
        tf.app.flags.DEFINE_string("ner_dictionary_file", config.NAMED_ENTITY_ROOT + "/vocab.txt", "Word2Vec Dictionary File.")
        tf.app.flags.DEFINE_string("ner_target_dictionary_file", config.NAMED_ENTITY_ROOT + "/ner_vocab.txt", "Target Word2Vec Dictionary File.")
        tf.app.flags.DEFINE_string("chiSquareBiDicPER_file", config.NAMED_ENTITY_ROOT + "/neBi_gramChiSquare_PER.txt",
                                   "Ne Bi_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("chiSquareBiDicLOC_file", config.NAMED_ENTITY_ROOT + "/neBi_gramChiSquare_LOC.txt",
                                   "Ne Bi_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("chiSquareBiDicORG_file", config.NAMED_ENTITY_ROOT + "/neBi_gramChiSquare_ORG.txt",
                                   "Ne Bi_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("chiSquareTriDicPER_file", config.NAMED_ENTITY_ROOT + "/neTri_gramChiSquare_PER.txt",
                                   "Ne Tri_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("chiSquareTriDicLOC_file", config.NAMED_ENTITY_ROOT + "/neTri_gramChiSquare_LOC.txt",
                                   "Ne Tri_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("chiSquareTriDicORG_file", config.NAMED_ENTITY_ROOT + "/neTri_gramChiSquare_ORG.txt",
                                   "Ne Tri_gram ChiSquare dic File")
        tf.app.flags.DEFINE_string("morBiDic_file", config.NAMED_ENTITY_ROOT + "/bi_gramFreqVector.txt",
                                   "sejong mor copurs Bi-Eumjul vector dic File")
        tf.app.flags.DEFINE_string("morTriDic_file", config.NAMED_ENTITY_ROOT + "/tri_gramFreqVector.txt",
                                   "sejong mor copurs Tri-Eumjul vector dic File")

        tf.app.flags.DEFINE_string("ner_test_file", config.NAMED_ENTITY_ROOT + "/unitNERTestDataSample.txt", "test file")
        tf.app.flags.DEFINE_string("ner_train_dir", config.NAMED_ENTITY_ROOT + "/model_new", "Training directory.")

        tf.app.flags.DEFINE_integer("ner_batch_size", 1, "Size of mini batch.")
        tf.app.flags.DEFINE_integer("ner_embedding_size", 50, "embedding_size")
        tf.app.flags.DEFINE_integer("ner_hidden_size", 128, "hidden_size")
        tf.app.flags.DEFINE_string("ner_cell_mode", "GRU", "cell_mode")
        tf.app.flags.DEFINE_integer("ner_num_epoch", 50, "number of epoch")
        tf.app.flags.DEFINE_float("ner_learning_rate", 0.0001, "learning rate")
        tf.app.flags.DEFINE_integer("ner_max_length", 105, "max_input_length")
        tf.app.flags.DEFINE_integer("ner_rate_per_checkpoint", 5, "percent rate per checkpoint.")
        tf.app.flags.DEFINE_integer("ner_epoch_per_checkpoint", 20, "epoch per checkpoint.")
        tf.app.flags.DEFINE_float("ner_dropout", 1.0, "dropout")
        tf.app.flags.DEFINE_integer("ner_num_layers", 1, "num_layers")

        tf.app.flags.FLAGS._parse_flags()
        self.FLAGS = tf.app.flags.FLAGS

        self.word2idx = {"<PADDING>": 0, "<UNK>": 1}
        self.idx2word = {0: "<PADDING>", 1: "<UNK>"}
        self.decode_word2idx = {"<PADDING>": 0}
        self.decode_idx2word = {0: "<PADDING>"}
        self.ner_tagDic = {"LOCATION": 0, "ORGANIZATION": 1, "PERSON": 2}

        self.chiSquareBiDic = {}
        self.chiSquareTriDic = {}
        self.morBiDic = {}
        self.morTriDic = {}
        self.chiIdx = 0

        # Dictionary Open
        with open(self.FLAGS.ner_dictionary_file, 'r') as inFile:
            for line in inFile:
                line = line.strip()
                # line = line.decode('utf-8')
                tokens = line.split()
                idx = len(self.word2idx)
                self.word2idx[tokens[0]] = idx
                self.idx2word[idx] = tokens[0]
        with open(self.FLAGS.ner_target_dictionary_file, 'r') as inFile:
            for line in inFile:
                line = line.strip()
                # line = line.decode('utf-8')
                tokens = line.split()
                idx = len(self.decode_word2idx)
                self.decode_word2idx[tokens[0]] = idx
                self.decode_idx2word[idx] = tokens[0]
        with open(self.FLAGS.chiSquareBiDicPER_file, 'r') as chiSquareBi:
            for line in chiSquareBi:
                line = line.strip()
                biWord = line.split("\t")[0]
                # biWord = biWord.decode('utf-8')
                self.chiSquareBiDic[biWord] = self.chiIdx
                self.chiIdx += 1
        with open(self.FLAGS.chiSquareBiDicLOC_file, 'r') as chiSquareBi:
            for line in chiSquareBi:
                line = line.strip()
                biWord = line.split("\t")[0]
                # biWord = biWord.decode('utf-8')
                self.chiSquareBiDic[biWord] = self.chiIdx
                self.chiIdx += 1
        with open(self.FLAGS.chiSquareBiDicORG_file, 'r') as chiSquareBi:
            for line in chiSquareBi:
                line = line.strip()
                biWord = line.split("\t")[0]
                # biWord = biWord.decode('utf-8')
                self.chiSquareBiDic[biWord] = self.chiIdx
                self.chiIdx += 1
        self.chiIdx = 0
        with open(self.FLAGS.chiSquareTriDicPER_file, 'r') as chiSquareTri:
            for line in chiSquareTri:
                line = line.strip()
                triWord = line.split("\t")[0]
                # triWord = triWord.decode('utf-8')
                self.chiSquareTriDic[triWord] = self.chiIdx
                self.chiIdx += 1
        with open(self.FLAGS.chiSquareTriDicLOC_file, 'r') as chiSquareTri:
            for line in chiSquareTri:
                line = line.strip()
                triWord = line.split("\t")[0]
                # triWord = triWord.decode('utf-8')
                self.chiSquareTriDic[triWord] = self.chiIdx
                self.chiIdx += 1
        with open(self.FLAGS.chiSquareTriDicORG_file, 'r') as chiSquareTri:
            for line in chiSquareTri:
                line = line.strip()
                triWord = line.split("\t")[0]
                # triWord = triWord.decode('utf-8')
                self.chiSquareTriDic[triWord] = self.chiIdx
                self.chiIdx += 1
        with open(self.FLAGS.morBiDic_file, 'r') as morBi:
            for line in morBi:
                line = line.strip()
                morBiWord = line.split("\t")[0]
                # morBiWord = morBiWord.decode('utf-8')
                morBiFreq = line.split('\t')[1].split()
                self.morBiDic[morBiWord] = morBiFreq
        with open(self.FLAGS.morTriDic_file, 'r') as morTri:
            for line in morTri:
                line = line.strip()
                morTriWord = line.split("\t")[0]
                # morTriWord = morTriWord.decode('utf-8')
                morTriFreq = line.split('\t')[1].split()
                self.morTriDic[morTriWord] = morTriFreq

    def formatting_data(self, line):
        query = line
        query = re.sub("[0-9]", "0", query)
        #     sentence = tokens[1]
        #     answer = tokens[2]
        query = re.sub("[0-9]", "0", query)
        test_x = []

        for token in query.split():
            if token in self.word2idx:
                test_x.append(self.word2idx[token])
            else:
                test_x.append(self.word2idx["<UNK>"])

        if len(test_x) > self.FLAGS.ner_max_length:
            test_x = test_x[:self.FLAGS.ner_max_length]
        sequence_length = len(test_x)
        if sequence_length > self.FLAGS.ner_max_length:
            sequence_length = self.FLAGS.ner_max_length
        return (test_x, sequence_length)

    def create_model(self, args, session, isTest, keep_prob):
        model = gru_crf.GRUCRF(args, self.word2idx, self.decode_word2idx, 1040)

        ckpt = tf.train.get_checkpoint_state(self.FLAGS.ner_train_dir)
        if ckpt:
            file_name = ckpt.model_checkpoint_path + ".meta"
        if ckpt and tf.gfile.Exists(file_name):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            model.saver.restore(session, ckpt.model_checkpoint_path)
            print("Success Load!")

        else:
            print("Created model with fresh parameters.")
            session.run(tf.global_variables_initializer())
        return model

    def hasBiMorFreqDic(self, word):
        freqBiList = [0.0 for _ in range(8)]
        if word in self.morBiDic:
            freqList = self.morBiDic[word]
            freqSum = 0
            for i in freqList:
                freqSum += int(i)
            for i in range(len(freqList)):
                freqBiList[i] = (float(freqList[i]) / freqSum)
        return freqBiList

    def hasTriMorFreqDic(self, word):
        freqTriList = [0.0 for _ in range(8)]
        if word in self.morTriDic:
            freqList = self.morTriDic[word]
            freqSum = 0
            for i in freqList:
                freqSum += int(i)
            for i in range(len(freqList)):
                freqTriList[i] = (float(freqList[i]) / freqSum)
        return freqTriList

    def hasBiDic(self, word, neBiChiDic):
        if word in self.chiSquareBiDic:
            self.chiIdx = self.chiSquareBiDic[word]
            neBiChiDic[self.chiIdx] = 1.0
        return neBiChiDic

    def hasTriDic(self, word, neTriChiDic):
        if word in self.chiSquareTriDic:
            self.chiIdx = self.chiSquareTriDic[word]
            neTriChiDic[self.chiIdx] = 1.0
        return neTriChiDic

    def test_line(self, line, sess, model):
        nerResultList = []
        inputEumjuls = self.make_EumjulSet(line)
        splitEumList = []
        if len(inputEumjuls.split('\t')[0].split()) > 100:
            splitEumList = self.split_data(inputEumjuls)
        else:
            splitEumList.append(inputEumjuls.split('\t')[0])

        for inputEumjul in splitEumList:
            test_x, sequence_length = self.formatting_data(inputEumjul)
            test_x, _, _, sequence_length = model.get_batch([(test_x, [], sequence_length)], self.FLAGS.ner_max_length)
            test_hasDic = []
            for col in range(len(test_x)):
                temp = []
                for row in range(len(test_x[col])):
                    temp.append(0.0)
                test_hasDic.append(temp)
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    dicFeature = [0.0 for _ in range(500)]
                    if self.idx2word[test_x[j][i]] != '<Start>' and self.idx2word[test_x[j][i]] != '<End>':
                        if test_x[j][i] != 0:
                            prevEumjul = self.idx2word[test_x[j][i - 1]]
                            currEumjul = self.idx2word[test_x[j][i]]
                            nextEumjul = self.idx2word[test_x[j][i + 1]]
                            dicFeature = self.hasBiDic(currEumjul + nextEumjul, dicFeature)
                            dicFeature = self.hasBiDic(prevEumjul + currEumjul, dicFeature)
                    test_hasDic[j][i] = dicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    dicFeature = [0.0 for _ in range(500)]
                    if self.idx2word[test_x[j][i]] != '<Start>' and self.idx2word[test_x[j][i]] != '<End>':
                        if len(test_x[j]) >= 5:
                            if test_x[j][i] != 0:
                                middleTriEumjul = self.idx2word[test_x[j][i - 1]] + self.idx2word[test_x[j][i]] + \
                                                  self.idx2word[
                                                      test_x[j][i + 1]]
                                if i < 2:
                                    rightTriEumjul = self.idx2word[test_x[j][i]] + self.idx2word[test_x[j][i + 1]] + \
                                                     self.idx2word[
                                                         test_x[j][i + 2]]
                                    dicFeature = self.hasTriDic(middleTriEumjul, dicFeature)
                                    dicFeature = self.hasTriDic(rightTriEumjul, dicFeature)
                                elif i > len(test_x[j]) - 3:
                                    leftTriEumjul = self.idx2word[test_x[j][i - 2]] + self.idx2word[test_x[j][i - 1]] + \
                                                    self.idx2word[
                                                        test_x[j][i]]
                                    dicFeature = self.hasTriDic(leftTriEumjul, dicFeature)
                                    dicFeature = self.hasTriDic(middleTriEumjul, dicFeature)

                                else:
                                    leftTriEumjul = self.idx2word[test_x[j][i - 2]] + self.idx2word[test_x[j][i - 1]] + \
                                                    self.idx2word[
                                                        test_x[j][i]]
                                    rightTriEumjul = self.idx2word[test_x[j][i]] + self.idx2word[test_x[j][i + 1]] + \
                                                     self.idx2word[
                                                         test_x[j][i + 2]]
                                    dicFeature = self.hasTriDic(leftTriEumjul, dicFeature)
                                    dicFeature = self.hasTriDic(middleTriEumjul, dicFeature)
                                    dicFeature = self.hasTriDic(rightTriEumjul, dicFeature)
                    test_hasDic[j][i] += dicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    morDicFeature = []
                    if self.idx2word[test_x[j][i]] != '<Start>' and self.idx2word[test_x[j][i]] != '<End>':
                        if test_x[j][i] != 0:
                            prevEumjul = self.idx2word[test_x[j][i - 1]]
                            currEumjul = self.idx2word[test_x[j][i]]
                            nextEumjul = self.idx2word[test_x[j][i + 1]]
                            morDicFeature = self.hasBiMorFreqDic(prevEumjul + currEumjul)
                            morDicFeature += self.hasBiMorFreqDic(currEumjul + nextEumjul)
                    if not morDicFeature:
                        morDicFeature = [0.0 for _ in range(16)]
                    test_hasDic[j][i] += morDicFeature
            for j in range(len(test_x)):
                for i in range(len(test_x[j])):
                    morDicFeature = []
                    if self.idx2word[test_x[j][i]] != '<Start>' and self.idx2word[test_x[j][i]] != '<End>':
                        if len(test_x[j]) >= 5:
                            if test_x[j][i] != 0:
                                middleTriEumjul = self.idx2word[test_x[j][i - 1]] + self.idx2word[test_x[j][i]] + \
                                                  self.idx2word[
                                                      test_x[j][i + 1]]
                                if i < 2:
                                    rightTriEumjul = self.idx2word[test_x[j][i]] + self.idx2word[test_x[j][i + 1]] + \
                                                     self.idx2word[
                                                         test_x[j][i + 2]]
                                    leftTriVector = [0.0 for _ in range(8)]
                                    morDicFeature = leftTriVector
                                    morDicFeature += self.hasTriMorFreqDic(middleTriEumjul)
                                    morDicFeature += self.hasTriMorFreqDic(rightTriEumjul)
                                elif i > len(test_x[j]) - 3:
                                    leftTriEumjul = self.idx2word[test_x[j][i - 2]] + self.idx2word[test_x[j][i - 1]] + \
                                                    self.idx2word[
                                                        test_x[j][i]]
                                    morDicFeature = self.hasTriMorFreqDic(leftTriEumjul)
                                    morDicFeature += self.hasTriMorFreqDic(middleTriEumjul)
                                    leftTriVector = [0.0 for _ in range(8)]
                                    morDicFeature += leftTriVector

                                else:
                                    leftTriEumjul = self.idx2word[test_x[j][i - 2]] + self.idx2word[test_x[j][i - 1]] + \
                                                    self.idx2word[
                                                        test_x[j][i]]
                                    rightTriEumjul = self.idx2word[test_x[j][i]] + self.idx2word[test_x[j][i + 1]] + \
                                                     self.idx2word[
                                                         test_x[j][i + 2]]
                                    morDicFeature = self.hasTriMorFreqDic(leftTriEumjul)
                                    morDicFeature += self.hasTriMorFreqDic(middleTriEumjul)
                                    morDicFeature += self.hasTriMorFreqDic(rightTriEumjul)
                    if not morDicFeature:
                        morDicFeature = [0.0 for _ in range(24)]
                    test_hasDic[j][i] += morDicFeature

            predict = model.predict_step(sess, test_x, test_hasDic, sequence_length, self.FLAGS.ner_dropout)
            #                 print predict
            strResult = ""
            for s in predict[0]:
                strResult += self.decode_idx2word[s] + " "
            print_result_set = self.restore(inputEumjul, strResult)
            nerResult = ""
            for i in print_result_set:
                nerResult += i + " "

            nerResultList.append(nerResult)
        return nerResultList

    def symbol(self, inputEumjul, predictEumjul):
        inputList = inputEumjul.split()
        predictList = predictEumjul.split()
        refienPredict = ""
        for i in range(len(inputList)):
            if inputList[i] == "<Start>" or inputList[i] == "<End>":
                predictList[i] = "#%#"
            elif inputList[i] == "<SP>":
                predictList[i] = "<SP>"
            elif inputList[i] != "<SP>" and (predictList[i] == "<SP>" or predictList[i] == "#%#"):
                predictList[i] = "O"
            refienPredict += predictList[i] + " "
        return refienPredict.strip()

    def restore(self, eumjulSet, predictSet):
        eumjulSet = eumjulSet.replace("<Start>", "")
        eumjulSet = eumjulSet.replace("<End>", "")
        eumjulSet = eumjulSet.strip()
        predictSet = predictSet.replace("#%#", "")
        predictSet = predictSet.strip()
        eojulWord = eumjulSet.split("<SP>")
        eojulTag = predictSet.split("<SP>")
        sentence = ""
        nerResult = []
        for i in range(len(eojulWord)):
            eumjulWord = eojulWord[i].strip().split(" ")
            eumjulTag = eojulTag[i].strip().split(" ")
            ner_word = ""
            ner_tag = ""
            temp = ""
            hasNER = False
            if len(eumjulWord) != len(eumjulTag):
                print(eumjulSet)
                print(predictSet)
            for j in range(len(eumjulWord)):
                if "B_" in eumjulTag[j]:
                    ner_word = eumjulWord[j]
                    ner_tag = eumjulTag[j]
                    if j == len(eumjulTag) - 1:
                        if hasNER:
                            temp = nerResult[len(nerResult) - 1] + ";" + ner_word + "@" + ner_tag
                            nerResult[len(nerResult) - 1] = temp
                        else:
                            temp = ner_word + "@" + ner_tag
                            nerResult.append(temp)
                        hasNER = True

                elif "I_" in eumjulTag[j]:
                    if len(eumjulWord) == 1:
                        ner_word = eumjulWord[j]
                        ner_tag = "I"
                        if hasNER:
                            temp = nerResult[len(nerResult) - 1] + ";" + ner_word + "@" + ner_tag
                            nerResult[len(nerResult) - 1] = temp
                        else:
                            temp = ner_word + "@" + ner_tag
                            nerResult.append(temp)
                        hasNER = True

                    elif (j == 0):
                        ner_word = eumjulWord[j]
                        ner_tag = "I"

                    elif (j == len(eumjulTag) - 1):
                        ner_word += eumjulWord[j]
                        if hasNER:
                            temp = nerResult[len(nerResult) - 1] + ";" + ner_word + "@" + ner_tag
                            nerResult[len(nerResult) - 1] = temp
                        else:
                            temp = ner_word + "@" + ner_tag
                            nerResult.append(temp)
                        hasNER = True
                    else:
                        ner_word += eumjulWord[j]
                else:
                    if ner_tag:
                        if hasNER:
                            temp = nerResult[len(nerResult) - 1] + ";" + ner_word + "@" + ner_tag
                            nerResult[len(nerResult) - 1] = temp
                        else:
                            temp = ner_word + "@" + ner_tag
                            nerResult.append(temp)
                        hasNER = True
                        ner_word = ""
                        ner_tag = ""

                    elif (j == len(eumjulTag) - 1 and not temp):
                        temp = "O"
                        nerResult.append(temp)
                        hasNER = True
                sentence += eumjulWord[j]
            sentence += " "
        return nerResult

    def split_data(self, line):
        line = line.strip()
        flag = True  # syllable\tne_tag
        if '\t' not in line:
            flag = False  # syllable
        splitEumList = []
        splitTagList = []
        if flag:
            eumjulSet = line.split('\t')[0]
            tagSet = line.split('\t')[1]
        else:
            eumjulSet = line

        while (len(eumjulSet.split()) > 99):
            eojulSet = eumjulSet.split(' <SP> ')
            if flag:
                eojultagSet = tagSet.split('<SP> ')
            eumjulList = []
            tagList = []
            for x in eojulSet:
                eumjulList += x.split() + ['<SP>']
            if flag:
                for x in eojultagSet:
                    tagList += x.split() + ['<SP>']
            eumjulSum = 0
            for i in range(len(eojulSet)):
                if eumjulSum + len(eojulSet[i].split()) + 1 < 100:
                    eumjulSum += len(eojulSet[i].split()) + 1
                else:
                    leftLine = ' '.join(eumjulList[:eumjulSum - 1] + ["<End>"])
                    rightLine = ' '.join(["<Start>"] + eumjulList[eumjulSum:-1])
                    eumjulSet = rightLine
                    splitEumList.append(leftLine)
                    if (len(eumjulSet.split()) < 100):
                        splitEumList.append(rightLine)
                    if flag:
                        leftTag = ' '.join(tagList[:eumjulSum - 1] + ["#%#"])
                        splitTagList.append(leftTag)
                        rightTag = ' '.join(["#%#"] + tagList[eumjulSum:-1])
                        tagSet = rightTag
                        if (len(eumjulSet.split()) < 100):
                            splitTagList.append(rightTag)
                    break
        if flag:
            return splitEumList, splitTagList
        else:
            return splitEumList

    def make_EumjulSet(self, line):
        # line = line.decode('utf-8')
        eumjulSet = ""
        for i in range(len(line)):
            if line[i] == " ":
                eumjulSet += "<SP> "
            else:
                eumjulSet += line[i] + " "
        eumjulSet = "<Start> " + eumjulSet + "<End>"
        return eumjulSet

    def ner_model_road(self,):
        sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True)))
        model = self.create_model(self.FLAGS, sess, True, 1.0)
        model.ner_batch_size = 1
        return sess, model

if __name__ == "__main__":
    ner = NER()
    sess, ner_model = ner.ner_model_road()
    str_list = ["건우는 춘천에서 강원대학교를 다닌다.","세희는 춘천에서 강원대학교를 다닌다.","민경이는 춘천에서 강원대학교를 다닌다.","신수는 춘천에서 강원대학교를 다닌다."]
    for input in str_list:
        print(input)
        nerResultList = ner.test_line(input, sess, ner_model)
        #ner.test_line은 list를 반환
        for line in nerResultList:
            print(line)
