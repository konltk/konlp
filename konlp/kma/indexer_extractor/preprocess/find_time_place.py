# -*- coding:utf-8 -*-
"""
색인어 추출을 위해 문장의 시제 용언의 위치를 찾아 주는 모듈
"""
from konlp.kma.indexer_extractor import config


class TimePlace(object):
    """
        문장에서 보조 용언의 위치를 찾는 모듈
    """
    # 시제정보 파일을 읽음
    def __init__(self):
        self.time_datas = []
        time_data = open(config.TIME_DATA, 'r', encoding='UTF8')
        for line in time_data.readlines():
            line = line.replace("\ufeff", "")
            self.time_datas.append(line.strip().split("\t"))
        time_data.close()

        # # 시제 위치 파악
        # ex ) 밥을 먹었어
        # T#1 과거 - 었
        # -> [['T#1', (3, 1)]]
        # T#1 - 과거
        # start = 3번쨰 형태소
        # size = 1
        # morpheme_word = [['밥/NNG', '을/JKO'], ['먹/VV', '었/EP', '어/EC']]
    def find_time_word_in_query(self, morpheme_word):
        """
        형태소 분석된 결과에서 시제 용언의 위치를 찾는 함수
        Args:
            morpheme_word (list) : 문장의 형태소 분석 결과
        Returns:
            List : 시제 용언의 부호와 위치, 길이
        """
        morp_to_str = ""
        for eojeol in morpheme_word:
            for word in eojeol:
                word_token = word.split('/')
                morp_to_str = morp_to_str + word_token[0] + ' '
            morp_to_str = morp_to_str[:-1]
            morp_to_str = morp_to_str + "\t"
        morp_to_str = morp_to_str[:-1]

        time = []
        time_place = []
        for time_data in self.time_datas:
            substitution_word = time_data[0]
            for time_data_idx in range(2, len(time_data)):
                time_word = time_data[time_data_idx]
                str_eojeol = morp_to_str.split("\t")

                start_num = 0
                for eojeol_idx, _ in enumerate(str_eojeol):
                    word_token = str_eojeol[eojeol_idx].split()
                    eojeol = str_eojeol[eojeol_idx].replace(" ", "")
                    time_word_temp = time_word
                    if time_word_temp in eojeol:
                        size = 1

                        for token in word_token:
                            if token == time_word_temp or time_word_temp in token:
                                time.append(substitution_word)
                                place = (start_num, size)
                                time_place.append(place)
                                start_num = start_num + size
                            elif token in time_word_temp:
                                time_word_temp = time_word_temp.replace(token, "", 1)
                                size = size + 1
                            else:
                                start_num = start_num +1
                    else:
                        start_num = start_num + len(word_token)


         # 시제용언 동일 위치에 중복되면 가장 긴 시제용언을 사용
         # time = ['T#1', ... ]  , modal_place = [(4,1), ...]
        self._overlap_remove(time, time_place)

        result_list = []
        for idx, _ in enumerate(time_place):
            result = []
            result.append(time[idx])
            result.append(time_place[idx])
            result_list.append(result)
        return result_list

     # 시제 위치,크기를 보고 최장일치 적용
     # ex) 밥을 먹었었어.   었 , 었었 모두 과거를 의미하는 T#1
     # 가장 긴 "었었"을 T#1으로 치환
    def _overlap_remove(self, time, time_place):
        remove_idx = []
        for idx in range(len(time)):
            start = time_place[idx][0]
            end = start + time_place[idx][1] - 1
            current = (start, end)

            for compare_place_idx in range(idx + 1, len(time)):
                start = time_place[compare_place_idx][0]
                end = start + time_place[compare_place_idx][1] - 1
                compare = (start, end)
                if current[0] <= compare[0] and current[1] >= compare[1]:
                    remove_idx.append(compare_place_idx)
                elif current[0] >= compare[0] and current[1] < compare[1]:
                    remove_idx.append((idx))
                    break

        remove_idx = list(set(remove_idx))
        remove_idx.reverse()
        for idx in remove_idx:
            time.remove(time[idx])
            time_place.remove(time_place[idx])
