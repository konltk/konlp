from konlp.kma.indexer_extractor.utils.gru_crf_NER.kacteil_ner import KacteilNER
from konlp.kma.indexer_extractor import config
from jnius import autoclass
import os

class NLU(object):
    def __init__(self):
        # 형태소 분석기 불러오기(Java)
        self._load_morpheme_analyzer()

        # 개체명 인식기 불러오기(Python3 Tensorflow 1.4 이상)
        self._load_named_entity_recognizer()
        print ("# NLU Load Success!")

    def _load_morpheme_analyzer(self):
        print ("# Morpheme Analyzer Loading...")
        morpheme_java_class = autoclass('kacteil.kma.MorphemeAnalysis')
        self.morpheme_analyzer = morpheme_java_class(True, False, False)
        print(config.MORPHEME_ANALYSIS_DATA)
        print(os.listdir(config.MORPHEME_ANALYSIS_DATA))
        self.morpheme_analyzer.loadFile(config.MORPHEME_ANALYSIS_DATA)

    def _load_named_entity_recognizer(self):
        print("# Named Entity Recognizer Loading...")
        self.kac_ner = KacteilNER(config.NAMED_ENTITY_DATA)

    def named_entity_recognize(self, query):
        result = self.kac_ner.test_line(query)
        return result[0]

    def morpheme_analysis(self, query):
        analysed_morpheme = self.morpheme_analyzer.getMorpheme(query)
        result = []
        for i in range(analysed_morpheme.size()):
            source = analysed_morpheme[i]
            word_list = source.getFirst()
            pos_list = source.getSecond()

            eojeol = []
            for word, pos in zip(word_list[1:], pos_list[1:]):
                eojeol.append("%s/%s" % (word, pos))
            result.append(eojeol)
        return result

    def get_morpheme(self, str):
        result = self.morpheme_analysis(str)
        morpheme = []
        for token in result:
            for morp in token:
                morpheme.append(morp)
        return morpheme
