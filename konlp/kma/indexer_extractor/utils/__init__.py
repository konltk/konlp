from konlp.kma.indexer_extractor import config
import jnius_config
if not jnius_config.vm_running:
    jnius_config.add_classpath(config.EXTERNAL_LIBRARY_PATH + "/*")