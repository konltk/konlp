# -*- coding: utf-8 -*-
"""
색인어 추출을 위해 문장의 보조 용언의 위치를 찾아 주는 모듈
"""
from konlp.kma.indexer_extractor import config

class ModalPlace(object):
    """
        문장에서 보조 용언의 위치를 찾는 모듈
    """
    modal_datas = []
    # 보조용언 파일을 읽음
    def __init__(self):
        modal_file = open(config.MODAL_FILE, 'r', encoding='UTF8')
        for line in modal_file.readlines():
            line = line.replace("\ufeff", "")
            self.modal_datas.append(line.strip().split("\t"))
        modal_file.close()


    # # 보조용언 위치 파악
    # ex ) 날씨가 정말 더운 듯 하다!
    # M#31 추측 - ㄴ 듯 하
    # -> [['M#31',(4,3)]]
    # M#31 - 추측
    # start = 4번쨰 형태소
    # size = 3
    # morpheme_word  = [['밥/NNG'], ['하/VV', '기/ETN'], ['때문/NNB', '이/VCP', '다/EC']] 형태소 분석된 결과
    def find_modal_word_in_query(self, morpheme_word):
        """
        형태소 분석된 결과에서 보조 용언의 위치를 찾는 함수
        Args:
            morpheme_word (list) : 문장의 형태소 분석 결과
        Returns:
            List : 보조 용언의 부호와 위치, 길이
        """
        morp_to_str = ""
        for eojeol in morpheme_word:
            for word in eojeol:
                word_token = word.split('/')
                morp_to_str = morp_to_str + word_token[0] + ' '
            morp_to_str = morp_to_str[:-1]
            morp_to_str = morp_to_str + "\t"
        morp_to_str = morp_to_str[:-1]

        substitution = []
        modal_place = []
        for modal_data in self.modal_datas:
            substitution_word = modal_data[0]

            for modal_data_idx in range(2, len(modal_data)):
                modal_word = modal_data[modal_data_idx]
                modal_word_token = modal_word.split()
                str_eojeol = morp_to_str.split("\t")

                place_num = 0
                for eojeol_idx, _ in enumerate(str_eojeol):
                    word_token = str_eojeol[eojeol_idx].split()
                    if len(modal_word_token) == 1:
                        for word in word_token:
                            if word == modal_word_token[0]:
                                place = (place_num, 1)
                                if place in modal_place:
                                    overlap_index = modal_place.index(place)
                                    substitution[overlap_index] = substitution[overlap_index]\
                                                                  +'###'+substitution_word
                                else:
                                    substitution.append(substitution_word)
                                    modal_place.append(place)
                                break
                            place_num = place_num +1
                    else:
                        if word_token[len(word_token)-1] == modal_word_token[0] and len(str_eojeol)\
                                - eojeol_idx -1 >= len(modal_word_token) -1:
                            place_num = place_num + len(word_token) - 1
                            size = 1
                            check = True
                            for modal_word_token_idx in range(1, len(modal_word_token)):
                                if modal_word_token[modal_word_token_idx] not in \
                                        str_eojeol[eojeol_idx + modal_word_token_idx]\
                                                .replace(" ", ""):
                                    check = False
                                    break

                                modal_token = modal_word_token[modal_word_token_idx]
                                if modal_word_token_idx != len(modal_word_token)-1:
                                    next_word = str_eojeol[eojeol_idx + modal_word_token_idx]\
                                        .replace(" ", "")
                                    if next_word != modal_token:
                                        check = False

                                next_word_token = str_eojeol[eojeol_idx +
                                                             modal_word_token_idx].split()

                                if modal_token:
                                    next_word_check = False
                                    for next_token in next_word_token:
                                        if next_token not in modal_token:
                                            break
                                        else:
                                            if next_token == modal_token[:len(next_token)]:
                                                modal_token.replace(next_token, "")
                                                size = size + 1
                                                next_word_check = True
                                            else:
                                                break
                                    check = next_word_check
                            if check:
                                place = (place_num, size)
                                if place not in modal_place:
                                    substitution.append(substitution_word)
                                    modal_place.append(place)
                        else:
                            place_num = place_num + len(word_token)


        # 보조용언 동일 위치에 있으면 가장 긴 보조용언을 사용
        # substitution = ['M#3', ... ]  , modal_place = [(4,3), ...]
        # modal_place = ['밥/NNG', '하/VV', '기/ETN', '때문/NNB', '이/VCP', '다/EC']
        # 형식에서의 (start_idx,size)를 의미
        self._longest_coincidence(substitution, modal_place)

        result_list = []
        for idx, _ in enumerate(modal_place):
            result = []
            result.append(substitution[idx])
            result.append(modal_place[idx])
            result_list.append(result)

        return result_list

     # 보조용언 위치,크기를 보고 최장일치 적용
     # ex) 밥 하기 때문이다  -> substitution = ['M#16', 'M#24']  modal_place = [(2, 1), (2, 3)]
     # modal_place = ['밥/NNG', '하/VV', '기/ETN', '때문/NNB', '이/VCP', '다/EC']
     # 형식에서의 (start_idx,size)를 의미
    def _longest_coincidence(self, substitution, modal_place):
        remove_idx = []
        for place_idx, _ in enumerate(modal_place):
            start = modal_place[place_idx][0]
            end = start  + modal_place[place_idx][1] -1
            current = (start, end)
            for compare_place_idx in range(place_idx+1, len(modal_place)):
                start = modal_place[compare_place_idx][0]
                end = start + modal_place[compare_place_idx][1] - 1
                compare = (start, end)
                if current[0] <= compare[0] and current[1] >= compare[1]:
                    remove_idx.append(compare_place_idx)
                elif current[0] >= compare[0] and current[1] < compare[1]:
                    remove_idx.append(place_idx)
                    break

        remove_idx = list(set(remove_idx))
        remove_idx.reverse()

        for idx in remove_idx:
            substitution.remove(substitution[idx])
            modal_place.remove(modal_place[idx])
