KoNLP 설치하기 
====================

.. sourcecode:: 

	konlp는 현재 python 3.5를 지원합니다.

Unix (Ubuntu 14.04, 16.04)
--------------------------

1. 종속 패키지 설치 

.. sourcecode:: bash

	$ sudo apt-get install python3-dev  

2. KoNLP 설치 

	1) pip

	.. sourcecode:: bash

		$ sudo pip3 install konlp  

	2) github

	.. sourcecode:: bash

		$ sudo git clone https://github.com/konltk/konlp  
		$ cd konlp  
		$ sudo python3 setup.py install  

3. 실행하기 

.. sourcecode:: python

	>>> from konlp.kma.klt2000 import klt2000
	>>> k = klt2000()
	>>> k = k.pos('나는 사과를 먹었다')
	>>> k = k.morphs('나는 사과를 먹었다')
	>>> k = k.nouns('나는 사과를 먹었다')


Windows
-------

...


Installing Third-Party Software
-------------------------------

...
