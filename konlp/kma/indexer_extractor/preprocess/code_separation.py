# -*- coding: utf-8 -*-
"""
색인어 추출을 하기 전에 문장에서 불필요한 특수 문자를 제거하는 모듈
"""
import re


class Separation(object):
    """
    문장에서 불필요한 특수 문자를 구분하는 모듈
    """

    def __init__(self):
        self.sentence = ""

    # 중복 '?','!','.' 하나로 줄임  안녕!!!! -> 안녕!
    def _remove_overlap_signal(self):
        self.sentence = re.sub(r'[.]+', '. ', self.sentence)
        self.sentence = re.sub(r'[!]+', '! ', self.sentence)
        self.sentence = re.sub(r'[?]+', '? ', self.sentence)


    # 문자와 기호간 공백 추가 - [!?.] 제외
    # 안녕! - > 안녕!   "안녕" -> " 안녕 "
    def _put_a_space_between_word_and_code(self):

        char_idx_list = []
        for char_idx in range(len(self.sentence) - 1):
            if bool(re.search('[가-힣a-zA-Z0-9]', self.sentence[char_idx])):
                if char_idx != 0 and \
                        not bool(re.search('[가-힣a-zA-Z0-9\s]', self.sentence[char_idx - 1])):
                    if not (char_idx != len(self.sentence)-1 and
                            not bool(re.search('[가-힣a-zA-Z0-9\s]', self.sentence[char_idx + 1]))):
                        char_idx_list.append(char_idx)
                if not bool(re.search('[가-힣a-zA-Z0-9\s]', self.sentence[char_idx + 1])):
                    if char_idx == len(self.sentence) - 2:
                        if not bool(re.search('[.?!]', self.sentence[char_idx + 1])):
                            if not (char_idx != 0 and
                                    not bool(re.search('[가-힣a-zA-Z0-9]',
                                                       self.sentence[char_idx - 1]))):
                                char_idx_list.append(char_idx + 1)
                    else:
                        if not bool(re.search('[.?!]', self.sentence[char_idx + 1])):
                            if not (char_idx != 0 and
                                    not bool(re.search('[가-힣a-zA-Z0-9]',
                                                       self.sentence[char_idx - 1]))):
                                char_idx_list.append(char_idx + 1)
                        else:
                            if bool(re.search('[.?!]', self.sentence[char_idx + 1])) and\
                                    bool(re.search('["]', self.sentence[char_idx + 2])):
                                char_idx_list.append(char_idx + 2)
                            elif not bool(re.search('[가-힣a-zA-Z0-9\s]',
                                                    self.sentence[char_idx + 2])):
                                char_idx_list.append(char_idx + 1)
        char_idx_list.reverse()

        # 기호 문자 분리
        for idx in char_idx_list:
            self.sentence = self.sentence[:idx] + " " + self.sentence[idx:]

    # " 안녕 "  - > 안녕   불필요한 특수문자 제거
    def remove_needless_in_query(self, sentence):
        """
        입력 문장에서 불필요한 특수문자를 제거하는 함수
        Args:
            sentence (str) : 입력 문장
        Returns:
            Str : 불필요한 특수문자가 제거된 문장
        """
        self.sentence = sentence
        self._remove_overlap_signal()
        self._put_a_space_between_word_and_code()

        # 기호,문자가 분리된 Token이 기호인 경우 제거
        tokens = self.sentence.split()
        self.sentence = ""

        for token in tokens:
            check = True
            if len(token) == 1:
                if not bool(re.search('[가-힣]', token)):
                    check = False
                else:
                    self.sentence = self.sentence +" "+ token
            else:
                for char_idx, _ in enumerate(token):
                    if not bool(re.search('[가-힣a-zA-Z0-9]', token[char_idx])):
                        # 마지막 문자가
                        if char_idx == len(token) -1:
                            if not bool(re.search('[가-힣a-zA-Z0-9?!.]', token[char_idx])):
                                check = False
                                break
                        else:
                            check = False
                            break
                if check:
                    self.sentence = self.sentence +" "+ token

        self.sentence = self.sentence[1:]
        return self.sentence
