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
.. code::
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
    >>> simple_txt = "내 눈을 본다면 밤하늘의 별이 되는 기분을 느낄 수 있을 거야"
    >>> k.pos(simple_txt)
    ['나/1', '눈/1', '보/V', '밤하늘/N', '별/1', '되/V', '기분/N', '느끼/V', '수/1', '있/V', '거/1']
    >>> k.morphs(simple_txt)
    ['나', '눈', '보', '밤하늘', '별', '되', '기분', '느끼', '수', '있', '거']
    >>> k.nouns(simple_txt)
    ['나', '눈', '밤하늘', '별', '기분', '수', '거']
    >>> k.sent_tokenize('국민대학교 자연어처리 연구실에서 만든  파이썬기반 형태소 분석기입니다.많은 이용 부탁드립니다.')
    ['국민대학교 자연어처리 연구실에서 만든  파이썬기반 형태소 분석기입니다.', '많은 이용 부탁드립니다.']

**사용자 사전추가 방법:**
.. code::
	'기성용', '모더나' 등과 같이 미등록명사는 '기성', '모더' 등과 같이 형태소 분석 오류가 발생할 수 있습니다. 
	이 경우에 해당 명사를 아래 경로에 있는 'ham-usr.dic'에 "소팅순서에 맞게" 추가하면 됩니다.
	(주의) ham-usr.dic은 텍스트 파일이며, KS완성형(cp949) 한글코드로 저장해야 함! 
	 
	사용자 사전 경로 : 
	(파이썬이 설치된 경로)\Python38\Lib\site-packages\konlp\kma\klt2000\hdic\ham-usr.dic 
	
Example(사용자 사전 추가전):

	>>> from konlp.kma.klt2000 import klt2000
	>>> k = klt2000()
	>>> k.pos('기성용 모더나')
	['기성/N', '모더/K']

Example(사용자 사전 추가후):

	>>> from konlp.kma.klt2000 import klt2000
	>>> k = klt2000()
	>>> k.pos('기성용 모더나')
	['기성용/N', '모더나/N']
	
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
