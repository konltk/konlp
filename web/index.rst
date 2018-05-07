.. KoNLP documentation master file, created by
   sphinx-quickstart on Sun May  6 22:09:09 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KoNLTK(Korean Natural Language Toolkit) - KoNLP
===============================================

KoNLTK: Korean Natural Language ToolKit

KoNLTK는 python언어를 이용하여 언어 데이터 작업을 하기위한 좋은 플랫폼입니다. pos-tagging, auto spacing 등 텍스트 처리, 가공 라이브러리 세트에 대한 사용하기 쉬운 인터페이스가 제공됩니다.

KoNLTK는 전산 언어학의 주제와 함께 프로그래밍 기초를 소개하는 실제 안내서와 포괄적 인 API 문서로 언어 학자, 엔지니어, 학생, 교육자, 연구원 및 업계 사용자 모두에게 적합합니다. NLTK는 Linux에서 사용할 수 있습니다. 무엇보다 NLTK는 무료 오픈 소스 커뮤니티 중심 프로젝트입니다.


Some simple things you can do with konlp
----------------------------------------

Morphological analysis:

    >>> from konlp.kma.klt import klt
    >>> k = klt.KltKma()
    >>> simple_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> k.analyze(simple_txt)
    [('안녕하세요', [('안녕', 'N'), ('하', 't'), ('세요', 'e')]), ('.', [('.', 'q')]),
    ('국민대학교', [('국민대학교', 'N')]), ('자연어처리', [('자연어처리', 'N')]), 
    ('연구실입니다', [('연구실', 'N'), ('이', 'c'), ('습니다', 'e')]), 
    ('.', [('.', 'q')])]
    >>> k.morphs(simple_txt)
    ['안녕', '하', '세요', '.', '국민대학교', '자연어처리', '연구실', '이', '습니다', '.']
    >>> k.nouns(simple_txt)
    ['안녕', '국민대학교', '자연어처리', '연구실']

Automatic word spacing:

    >>> from konlp.tokenize import KltAsp
    >>> k = KltAsp()
    >>> k.asp(text="국민대학교자연어처리연구실")
    ['국민대학교', '자연어처리', '연구실']
    >>> k.asp(text="국민대학교자연어처리연구실", split=False)
    '국민대학교 자연어처리 연구실'
    >>> k.asp(text="국민대학교자연어처리연구실", split=True)
    ['국민대학교', '자연어처리', '연구실']

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
