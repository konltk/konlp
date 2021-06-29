.. KoNLP documentation master file, created by
   sphinx-quickstart on Sun May  6 22:09:09 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KoNLTK(Korean Natural Language Toolkit) - KoNLP
===============================================

KoNLTK: Korean Natural Language ToolKit

KoNLTK는 python 언어를 이용하여 한글 관련 언어처리 작업을 하기 위한 플랫폼입니다. 형태소 분석, 품사 태깅, 구문 분석, 자동 띄어쓰기 등 한글 텍스트 처리, 언어처리 관련 라이브러리들에 대해 사용하기 쉬운 사용자 인터페이스가 제공됩니다. KoNLTK는 포괄적인 API 문서로 언어학자, 엔지니어, 학생, 교육자, 연구원들에게 적합합니다. NLTK는 Linux에서 사용할 수 있습니다.

NLTK는 국내 자연어 처리 연구 분야의 NLP 전문가들이 연구-개발한 결과물을 다양한 응용 분야에서 쉽게 활용할 수 있도록 API를 제공하여
한글 및 한국어 관련 분야의 발전에 기여하고자 합니다.

KoNLP 플랫폼을 통해 제공되는 연구결과물은 연구-개발 및 비영리적인 목적으로 무료로 제공되며 구체적인 사항은 저작권자의 라이선스 정책을 확인하기 바랍니다.


Some simple things you can do with konlp
----------------------------------------

How to Install konlp:
.. code-block::
    JAVA >= 11, Python3(3.8 이하) 필요
    **Microsoft Visual C++ Build Tools 에러 발생시**
    https://visualstudio.microsoft.com/ko/vs/older-downloads/ 에서 재배포 가능  패키지 및 빌드 도구 설치
    필요

    #Windows
    pip install wheel
    pip install konlp
    
    #Linux
    pip3 install wheel
    pip3 install konlp

Morphological analysis:

    >>> from konlp.kma.klt2000 import klt2000
    >>> k = klt2000()
    >>> simple_txt = "국민대학교 자연어처리 연구실에서 만든  파이썬기반 형태소 분석기입니다."
    >>> k.pos(simple_txt)
    ['국민대학교/C', '자연어처리/C', '연구실/N', '만들/V', '파이썬기반/K', '형태소/N', '분석기/N']
    >>> k.morphs(simple_txt)
    ['국민대학교', '자연어처리', '연구실', '만들', '파이썬기반', '형태소', '분석기']
    >>> k.nouns(simple_txt)
    ['국민대학교', '자연어처리', '연구실', '파이썬기반', '형태소', '분석기']
    >>> k.sentences('''국민대학교 자연어처리 연구실에서 만든  파이썬기반 형태소 분석기입니다.많은 이용 
        부탁드립니다.''')# 문장 분리기
    ['국민대학교 자연어처리 연구실에서 만든  파이썬기반 형태소 분석기입니다.', '많은 이용 부탁드립니다.']

Display a parse tree:

    Later on, We are preparing...

.. toctree::
   :maxdepth: 2
   :caption: Contents:
  
   news
   install
   data
   contribute
   FAQ  <https://github.com/konltk/konlp/wiki/FQA>
   Wiki <https://github.com/konltk/konlp/wiki>
   API 
   HOWTO 
   


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
