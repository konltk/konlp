# -*- coding: utf-8 -*-
"""
데이터 색인에 필요한 색인어를 추출하는 모듈
"""

import re
from konlp.kma.api import KmaI
from konlp.kma.indexer_extractor import config
from konlp.kma.indexer_extractor.preprocess.code_separation import Separation
from konlp.kma.indexer_extractor.preprocess.find_modal_place import ModalPlace
from konlp.kma.indexer_extractor.preprocess.find_time_place import TimePlace
from konlp.kma.indexer_extractor.preprocess.unregistered_word_processing \
    import UnregisteredWordProcessing
from konlp.kma.indexer_extractor.utils import nlu


class IndexerExtractor(KmaI):
    """
    문장으로부터 색인어를 추출하는 모듈
    """
    def __init__(self):
        self._nlu = nlu.NLU()
        #질의패턴 사전 불러오기
        self._load_question_pattern()
        #query내 불필요한 특수문자 제거
        self._separation = Separation()
        #미등록어 처리
        self._unregistered_word_processing = UnregisteredWordProcessing()
        #보조용언 위치
        self._modal_place = ModalPlace()
        #시제용언 위치
        self._time_place = TimePlace()

    def _load_question_pattern(self):
        question_pattrn_file = open(config.QUESTION_PATTEN_FILE, 'r', encoding='utf8')
        lines = [line.strip() for line in question_pattrn_file.readlines()]
        question_pattrn_file.close()
        self.question_pattern_dic = set(lines)

    def _mapping_question_pattern(self, morpheme_result):
        """
        형태소 분석 결과에서 질의 패턴을 찾아
        질의 패턴 부호로 치환하는 함수
        Args:
            morpheme_result(list) : 형태소 분석 결과
        Returns:
            List : 질의 패턴 부분이 부호로 치환된 결과
        """
        last_eojeol = morpheme_result[-1]

        #두 형태소 패턴 찾기
        if len(last_eojeol) > 1:
            check_pattern = "+".join(last_eojeol[-2:])
            if check_pattern in self.question_pattern_dic:
                if last_eojeol[:-2]:
                    morpheme_result = morpheme_result[:-1] + \
                                      [last_eojeol[:-2]] + [[check_pattern + ' @Q']]
                else:
                    morpheme_result = morpheme_result[:-1] + [[check_pattern + ' @Q']]
        #한 형태소 패턴 찾기
        elif len(last_eojeol) == 1:
            check_pattern = last_eojeol[-1]
            if check_pattern in self.question_pattern_dic:
                if last_eojeol[:-1]:
                    morpheme_result = morpheme_result[:-1] + \
                                      [last_eojeol[:-1]] + [[check_pattern + ' @Q']]
                else:
                    morpheme_result = morpheme_result[:-1] + [[check_pattern + ' @Q']]
        return morpheme_result

    def _extract(self, input_str):
        """
        입력 문장에서 색인어 추출을 하는 함수
        Args:
            input_str (str) : 입력 문장

        Returns:
            List : [색인어 리스트], [형태소 분석된 리스트], [색인어 중 명사 리스트]
        """

        query = self._separation.remove_needless_in_query(input_str)
        if query.strip() == "":
            idx_term = ['이모티콘']
            feature_list = ['이모티콘 이모티콘']
            return idx_term, feature_list

        #형태소 분석
        morpheme_result = self._nlu.morpheme_analysis(query)
        #미등록어 처리
        self._unregistered_word_processing.unregistered_word_process(morpheme_result)
        #개체명 인식
        named_entity_result = self._nlu.named_entity_recognize(query)
        #IDX_TERM - 1. Q - pattern
        temp_result = self._mapping_question_pattern(morpheme_result)  # 질의패턴 파악
        #보조용언 치환부분
        modal_place = self._modal_place.find_modal_word_in_query(morpheme_result)

        for place_idx, _ in enumerate(modal_place):
            start = modal_place[place_idx][1][0]
            end = start + modal_place[place_idx][1][1] - 1
            substitution_word = modal_place[place_idx][0]

            place = 0
            for eojeol_idx, _ in enumerate(temp_result):
                for word_idx in range(len(temp_result[eojeol_idx])):
                    if start <= place and end >= place:
                        temp_result[eojeol_idx][word_idx] = temp_result[eojeol_idx][word_idx] \
                                                            + ' ' + substitution_word
                    place = place + 1

        # 시제용언 치환부분
        time_place = self._time_place.find_time_word_in_query(morpheme_result)
        for place_idx, _ in enumerate(time_place):
            start = time_place[place_idx][1][0]
            end = start + time_place[place_idx][1][1] - 1
            substitution_word = time_place[place_idx][0]

            place = 0
            for eojeol_idx, _ in enumerate(temp_result):
                for word_idx in range(len(temp_result[eojeol_idx])):
                    if start <= place and end >= place:
                        temp_result[eojeol_idx][word_idx] = temp_result[eojeol_idx][word_idx] \
                                                            + ' ' + substitution_word
                    place = place + 1

        # IDX_TERM - 2. ntt
        # 개체명 치환부분
        ner_tokens = named_entity_result.split()

        for token_index, token in enumerate(ner_tokens):
            if token.find("@") != -1:
                token = token.replace("@B_PERSON", " @PER")
                token = token.replace("@B_ORGANIZATION", " @ORG")
                token = token.replace("@B_LOCATION", " @LOC")
                token = token.replace("@B_DATE", " @DATE")
                token = token.replace("@B_TIME", " @TIME")
                token = token.replace("@I", " @I")

                token_spl = token.split()
                token_word = token_spl[0]
                ntt = token_spl[1]

                for temp_eojeol_word in temp_result[token_index]:
                    temp_eojeol_word_token = temp_eojeol_word.split('/')
                    if token_word == temp_eojeol_word_token[0]:
                        token = temp_eojeol_word + ' ' + ntt
                        break

                    if temp_result[token_index][-1] == temp_eojeol_word:
                        token_spl = token.split()
                        token = token_spl[0] + '/' + temp_eojeol_word_token[1] + ' ' + ntt

                temp_result[token_index] = [token]

        # 개체명 합치는 부분 ex) 파울로/NNP @PER 코엘료/NA @I -> 파울로코엘료/NA @PER
        merge_temp_result = []
        for tokens in temp_result:
            if tokens[0].find("@I") != -1:
                refine_token = tokens[0][:tokens[0].find("@")]

                prev_word_split_position = merge_temp_result[-1][0].find("@")
                prev_word = merge_temp_result[-1][0].split('/')
                prev_word = prev_word[0]
                prev_tag = merge_temp_result[-1][0][prev_word_split_position:]

                temp = prev_word + refine_token + prev_tag

                merge_temp_result[-1][0] = temp
            else:
                merge_temp_result.append(tokens)

        # [['말/NNG'], ['진짜/NNG'], ['못하/VX', 'ㄴ다/EF', './SF']]
        # -> ['말/NNG','진짜/NNG','못하/VX', 'ㄴ다/EF', './SF'] 형태소 리스트
        # 보조용언, 시제 합치기 위함
        mor_list = []
        for eojeol in merge_temp_result:
            for mor in eojeol:
                mor_list.append(mor)

        # 보조용언, 시제용언 합치기
        predicate_place = []
        size = 1

        # [형태소, 치환 어휘, 시작지점, 크기]
        for word_idx, _ in enumerate(mor_list):
            if 'M#' in mor_list[word_idx] or 'T#' in mor_list[word_idx]:
                word_token = mor_list[word_idx].split()
                predicate_info = [word_token[0], word_token[1], word_idx, size]
                predicate_place.append(predicate_info)

        predicate_place.reverse()
        predicate_remove_idx = []

        # 겹치는 부분 통합
        for current_idx in range(len(predicate_place) - 1):
            current_replace_word = predicate_place[current_idx][1]
            current_place = predicate_place[current_idx][2]

            prev_replace_word = predicate_place[current_idx + 1][1]
            prev_place = predicate_place[current_idx + 1][2]
            if current_replace_word == prev_replace_word:
                if current_place - prev_place == 1:
                    predicate_remove_idx.append(current_idx)
                    predicate_place[current_idx + 1][3] = predicate_place[current_idx + 1][3] + \
                                                          predicate_place[current_idx][3]
                    predicate_place[current_idx + 1][0] = predicate_place[current_idx + 1][0] +\
                                                          '#SPACE#' +\
                                                          predicate_place[current_idx][0]

        predicate_remove_idx.reverse()
        for remove_idx in predicate_remove_idx:
            predicate_place.remove(predicate_place[remove_idx])

        #stop_remove_list에 보조용언, 시제용언 처리
        for predicate_info in predicate_place:
            start = predicate_info[2]
            end = start + predicate_info[3] - 1
            mor_list[start] = predicate_info[0] + ' ' + predicate_info[1]
            for remove_idx in range(end, start, -1):
                mor_list.remove(mor_list[remove_idx])

        #불용어 처리 부분
        stopword_remove_list = []
        for mor in mor_list:
            if re.search(r'/[N]{1}|@|(/VV)|(/VA)|(/MAG)|(/MAJ)|(/SL)|'
                         r'(/SN)|(/VX)|(/VCP)|(/VCN)|(/IC)|(/XR)', mor):
                stopword_remove_list.append(mor)
            elif 'T#' in mor or 'M#' in mor:
                stopword_remove_list.append(mor)

        noun_list = []
        for mor in mor_list:
            if re.search(r'/[N]{1}|@', mor):
                noun_list.append(mor)

        return stopword_remove_list, morpheme_result, noun_list

    def analyze(self, string):
        """
        입력 문장에서 색인어 추출을 하는 함수
        Args:
            input_str (str) : 입력 문장
        Returns:
            List : [색인어 리스트]
        """

        idx_term = []
        stopword_remove_list, morpheme_result, _ = self._extract(string)
        for token in stopword_remove_list:
            split_tokens = token.split()
            if not len(split_tokens) == 2:
                idx_term.append(token)
            else:
                 # '###' => 보조용언이 겹치는 어휘부분 처리하기 위함 '이' M#16,M32
                if '###' in split_tokens[1]:
                    idx_term.append(split_tokens[1].strip().replace('###', ' '))
                elif '@Q' in split_tokens[1] != -1:
                    idx_term.append(split_tokens[1])
                elif split_tokens[1].find("@") != -1:
                    idx_term.append(token.strip())
                else:
                    idx_term.append(split_tokens[1].strip())

        #query가 모두 불용어라 idx_term 이 없는 경우 query 그대로 사용
        if not idx_term:
            idx_term = []
            for eojeol in morpheme_result:
                for char in eojeol:
                    idx_term.append(char)

        return idx_term

    def morphs(self, string):
        """
        추출된 색인어의 원형을 추출
        Args:
            input_str (str) : 입력 문장
        Returns:
            List : [색인어 원형 리스트]
        """
        original_starte_list = []
        stopword_remove_list, morpheme_result, _ = self._extract(string)

        #출력 포멧으로 변경
        for token in stopword_remove_list:
            split_tokens = token.split()
            if not len(split_tokens) == 2:
                original_starte_list.append(token)
            else:
                if '#SPACE#' in token:
                    token = token.replace('#SPACE#', ' ')
                    token = token.replace('###', ' ')
                token_spl = token.split()
                original_starte_list.append(' '.join(token_spl[:-1]))

        #query가 모두 불용어라 idx_term 이 없는 경우 query 그대로 사용
        if not original_starte_list:
            for eojeol in morpheme_result:
                for char in eojeol:
                    original_starte_list.append(char)

        return original_starte_list

    def nouns(self, string):
        """
        색인어의 명사 추출
        Args:
            input_str (str) : 입력 문장
        Returns:
            List : [색인어 중 명사 리스트]
        """
        _, _, nouns = self._extract(string)
        return nouns




