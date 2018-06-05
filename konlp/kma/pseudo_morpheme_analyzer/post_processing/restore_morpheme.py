"""
강원대학교 한국어 '의사 형태소 -> 일반 형태소' 복원 모듈
"""


class RestoredMorpheme(object):
    """
    강원대학교 한국어 '의사 형태소 -> 일반 형태소' 복원 클래스
    """
    @staticmethod
    def open_pre_analyzed_dic(pre_analyzed_dic_path):
        """기분석 사전 불러오기 함수
        Args:
            pre_analyzed_dic_path(str): 기분석 사전 경로
        return:
             pre_analyzed_dic: 기분석 사전
        """
        pre_analyzed_dic_f = open(pre_analyzed_dic_path, 'r')
        pre_analyzed_dic = {}
        for line in pre_analyzed_dic_f:
            line = line.strip()
            word = line.split("\t")[0]
            tags = line.split("\t")[1:]
            tag_freq_list = []
            for tag_freq in tags:
                tag = tag_freq.split("%&%")[0]
                freq = tag_freq.split("%&%")[1]
                tag_freq_list.append((tag, freq))
            pre_analyzed_dic[word] = tag_freq_list
        pre_analyzed_dic_f.close()
        return pre_analyzed_dic

    @staticmethod
    def open_restore_dic(restore_dic_path):
        """복원 사전 불러오기 함수
        Args:
            restore_dic_path(str): 복원 사전 경로
        return:
             restore_dic: 복원 사전
        """
        dic_f = open(restore_dic_path, 'r')
        restore_dic = {}
        for line in dic_f:
            line = line.strip()
            pseudo_mor = line.split("\t")[0]
            mor = line.split("\t")[1]
            restore_dic[pseudo_mor] = mor
        dic_f.close()
        return restore_dic

    @staticmethod
    def mor_tag_similarity(pseudo_morph_list, pre_analyzed_dic):
        """기분석 사전 적용 함수
        Args:
            pseudo_morph_list(list): 의사 형태소 분석 결과
            pre_analyzed_dic(dic): 기분석 사전
        return:
             pre_analyzed_dic[idx]: 기분석 사전 결과
        """
        mor_list = []
        for sym in pseudo_morph_list:
            sym = sym.replace("B_", "")
            sym = sym.replace("I_", "")
            if "+" in sym:
                mor_list += sym.split("+")
            else:
                mor_list.append(sym)
        dic_mor_list = []
        dic_mor_freq = []
        for dic_value, freq in pre_analyzed_dic:
            morph_pairs = dic_value.split(" + ")
            morph_list = []
            for mor_pair in morph_pairs:
                slash_idx = mor_pair.rfind("/")
                morpheme = mor_pair[slash_idx+1:]
                morph_list.append(morpheme)
            dic_mor_list.append(morph_list)
            dic_mor_freq.append(int(freq))
        equal_mor_list = []
        for dic_mor in dic_mor_list:
            equal_mor = 0
            for morpheme in dic_mor:
                if morpheme in mor_list:
                    equal_mor += 1
            equal_mor_list.append(equal_mor)
        max_length = equal_mor_list[0]
        max_idx = 0
        for i, _ in enumerate(equal_mor_list):
            if max_length < equal_mor_list[i]:
                max_length = equal_mor_list[i]
                max_idx = i
        count = 0
        for temp in equal_mor_list:
            if temp == max_length:
                count += 1
        if count > 1:
            freq_max_idx = 0
            for i, _ in enumerate(equal_mor_list):
                if equal_mor_list[i] == max_length:
                    if dic_mor_freq[i] > max_length:
                        freq_max_idx = i
            return pre_analyzed_dic[freq_max_idx][0]
        else:
            return pre_analyzed_dic[max_idx][0]

    @staticmethod
    def symbol_change(syllables, pseudo_morph):
        """기본 기호('<Start>', '<SP>','<End>')가 잘 못 분석된 경우 수정하는 함수
        Args:
            syllables(str): 음절 단위 입력 문장
            pseudo_morph(str): 의사 형태소 분석 결과
        return:
             post_pseudo_morpheme: 기본 기호 수정된 의사 형태소 분석 결과
        """
        sen_list = syllables.split()
        morph_list = pseudo_morph.split()
        for i, _ in enumerate(sen_list):
            if sen_list[i] == "<Start>":
                morph_list[i] = "#%#"
            elif sen_list[i] == "<End>":
                morph_list[i] = "#%#"
            elif sen_list[i] == "<SP>":
                morph_list[i] = "<SP>"
        post_pseudo_morpheme = ""
        for morph in morph_list:
            post_pseudo_morpheme += morph+" "
        return post_pseudo_morpheme.strip()

    def restore_morpheme(self, syllables, pseudo_morph, restore_dic, pre_analyzed_dic):
        """형태소 복원 함수
        Args:
            syllables(str): 음절 단위 입력 문장
            pseudo_morph(str): 의사 형태소 분석 결과
            restore_dic(dic): 복원 사전
            pre_analyzed_dic(dic): 기분석 사전
        return:
            morph_result_list: 복원된 형태소 분석 결과
        """
        pseudo_morph = self.symbol_change(syllables, pseudo_morph)
        syllables = syllables.replace("<Start>", "").replace("<End>", "").strip()
        pseudo_morph = pseudo_morph.replace("#%#", "").strip()

        words = syllables.split(" <SP> ")
        morph_tags = pseudo_morph.split(" <SP> ")
        morph_result_list = []
        for i, _ in enumerate(words):
            morph_result = ""
            syllable_list = words[i].split()
            pseudo_morph_list = morph_tags[i].split()
            eojeol = words[i].replace(" ", "")
            if eojeol in pre_analyzed_dic:
                if len(pre_analyzed_dic[eojeol]) > 1:
                    morph_result_list.append(self.mor_tag_similarity(
                        pseudo_morph_list, pre_analyzed_dic[eojeol]))
                else:
                    morph_result_list.append(pre_analyzed_dic[eojeol][0][0])
                continue
            word = ""
            tag = ""
            prev_tag = ""
            irregular_flag = False
            for j, _ in enumerate(pseudo_morph_list):
                if j > 0:
                    if "_" in pseudo_morph_list[j-1]:
                        if "+" in pseudo_morph_list[j-1]:
                            prev_tag = pseudo_morph_list[j-1].split("+")[1]
                        else:
                            prev_tag = pseudo_morph_list[j-1].split("_")[1]
                    else:
                        prev_tag = ""
                temp = ""
                if "_" in pseudo_morph_list[j]:
                    temp = pseudo_morph_list[j].split("_")[1]
                if temp == prev_tag:
                    pseudo_morph_list[j] = "I"

                if '+' in pseudo_morph_list[j]:
                    if word:
                        if "I" in tag:
                            if word+"/"+tag in restore_dic:
                                morph_result += restore_dic[word + "/" + tag] + " + "
                            elif word+"/"+tag not in restore_dic:
                                morph_result += word+"/NA + "
                            word = ""
                            tag = ""
                        elif "I" not in pseudo_morph_list[j]:
                            if word+"/"+tag in restore_dic:
                                morph_result += restore_dic[word + "/" + tag] + " + "
                            else:
                                if "_" in tag:
                                    tag = tag.split("_")[1]
                                    if "+" in tag:
                                        tag = tag.split("+")[0]
                                morph_result += word + "/" + tag + " + "
                            word = ""
                            tag = ""
                        elif "B" in pseudo_morph_list[j]:
                            if syllable_list[j]+"/"+pseudo_morph_list[j] in restore_dic:
                                morph_result += restore_dic[syllable_list[j]+"/"
                                                            +pseudo_morph_list[j]]+" + "
                            elif not syllable_list[j]+"/"+pseudo_morph_list[j] in restore_dic:
                                if "B_NY" in pseudo_morph_list[j]:
                                    word += syllable_list[j]
                                    tag += pseudo_morph_list[j]
                                    irregular_flag = True
                                    continue
                            word = ""
                            tag = ""
                    word += syllable_list[j]
                    tag += pseudo_morph_list[j]
                    irregular_flag = True
                elif "B_" in pseudo_morph_list[j]:
                    if word:
                        if "I" in tag:
                            if word+"/"+tag in restore_dic:
                                morph_result += restore_dic[word+"/"+tag]+" + "
                            elif word+"/"+tag not in restore_dic:
                                if "+" in tag or "I" in tag:
                                    morph_result += word + "/NA + "
                                else:
                                    morph_result += word + "/" + tag
                        else:
                            if word+"/"+tag in restore_dic:
                                morph_result += restore_dic[word+"/"+tag]+" + "
                            else:
                                if "_" in tag:
                                    tag = tag.split("_")[1]
                                    if "+" in tag:
                                        tag = tag.split("+")[0]
                                morph_result += word+"/"+tag+" + "
                        irregular_flag = False
                        word = ""
                        tag = ""

                    word += syllable_list[j]
                    tag += pseudo_morph_list[j]
                elif "I" in pseudo_morph_list[j]:
                    if irregular_flag:
                        word += syllable_list[j]
                        tag += pseudo_morph_list[j]
                    else:
                        word += syllable_list[j]

                if j == len(pseudo_morph_list)-1:
                    if word:

                        if word+"/"+tag in restore_dic:
                            morph_result += restore_dic[word+"/"+tag]
                        else:
                            if "+" in tag or "I" in tag:
                                morph_result += word + "/NA"
                            else:
                                if "_" in tag:
                                    tag = tag.split("_")[1]
                                    if "+" in tag:
                                        tag = tag.split("+")[0]
                                morph_result += word + "/" + tag
                        irregular_flag = False
                        word = ""
                        tag = ""
            morph_result_list.append(morph_result)
        return morph_result_list

    @staticmethod
    def sen_restore(syllables):
        """음절 단위 문장을 일반 문장으로 복원하는 함수
        Args:
            syllables(str): 음절 단위 입력 문장
        return:
            restored_sentence: 일반 문장
        """
        restored_sentence = ""
        syllables = syllables.replace("<Start>", "").replace("<End>", "")
        for syllable in syllables.split():
            if syllable == "<SP>":
                restored_sentence += " "
            else:
                restored_sentence += syllable
        return restored_sentence
