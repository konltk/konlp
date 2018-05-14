import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

EXTERNAL_LIBRARY_PATH = ROOT_DIR+"/lib"

MORPHEME_ANALYSIS_DATA = ROOT_DIR+"/resource/morpheme"

NAMED_ENTITY_ROOT = ROOT_DIR+"/utils/gru_crf_NER"
NAMED_ENTITY_DATA = ROOT_DIR+"/utils/gru_crf_NER/model_new"

QUESTION_PATTEN_FILE = ROOT_DIR+"/preprocess/data/question_pattern.txt"
MODAL_FILE = ROOT_DIR+"/preprocess/data/modal_data.txt"
TIME_DATA = ROOT_DIR+"/preprocess/data/time_data.txt"
