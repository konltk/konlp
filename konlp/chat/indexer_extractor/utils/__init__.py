import jnius_config
from konlp.chat.indexer_extractor import config

if not jnius_config.vm_running:
    jnius_config.add_classpath(config.EXTERNAL_LIBRARY_PATH + "/*")