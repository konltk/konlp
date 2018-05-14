# -*- coding:utf-8 -*-
"""
색인어 추출하기 전에 형태소 분석 결과 중 미등록어인 어휘를 앞 3글자만 남기는 모듈
"""

class UnregisteredWordProcessing(object):
    """
    형태소 분석 결과가 미등록어인 어휘를 앞 3글자만 남기는 모듈
    """
    def unregistered_word_process(self, morpheme_word):
        """
        형태소 분석된 결과에서 미등록어 어휘를 앞 3글자만 남기는 함수
        Args:
            morpheme_word (list) : 문장의 형태소 분석 결과
        Returns:
        """
        for eojeol_mor_idx, _ in enumerate(morpheme_word):
            for mor_idx, _ in enumerate(morpheme_word[eojeol_mor_idx]):
                mor_spl = morpheme_word[eojeol_mor_idx][mor_idx].split("/")
                if mor_spl[1] == "NA" and len(mor_spl[0]) > 3:
                    morpheme_word[eojeol_mor_idx][mor_idx] = mor_spl[0][0:3] + "/" + mor_spl[1]
