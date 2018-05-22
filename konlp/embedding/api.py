# -*- coding: utf-8 -*-
# Korean Natural Language Toolkit: Korean Embedding Model Interface
# 
# Author: GeonYeong Kim <uhi7074@gmail.com>
#
# Contributors: 
# URL: <http://konltk.org/>
# For license information, see LICENSE.TXT

from abc import ABCMeta, abstractmethod
from six import add_metaclass


@add_metaclass(ABCMeta)
class abstract_embedding_model:
	"""
	한국어 임베딩 모델 인터페이스
	so파일 사용시 상속 후 init부분에 따로 구현
	"""
	
	@abstractmethod
	def train(self, input, vocab, output, save_type, size=100, negative_sampling=5, lr=0.025, sample=0.00001, window_size=5, min_count=5, threads=8, iter=1):
		"""
		문장들을 입력받아 워드 임베딩을 학습합니다.
		
		[description]
		:param input: 학습할 코퍼스 위치
		:type input: string
		:param vocab: 코퍼스에 등장하는 단어들을 저장할 위치
		:type vocab: string
		:param output: 학습한 모델을 저장할 경로
		:type output: str
		:param save_type: ('w' or 'b'), 모델을 어떤 방식으로 저장할지 결정, w=txt, b=binary
		:type save_type: char
		:param size: 학습할 벡터의 사이즈, default = 100
		:type size: int
		:param negative_sampling: negative_sampling, default = 5 (0=ns를 사용하지 않음)
		:type negative_sampling: int
		:param lr: learning rate, default = 0.025
		:type lr: float
		:param sample: 높은 빈도수의 단어들을 학습에서 랜덤하게 제외합니다., default = 0.00001
		:type sample: float
		:param window_size: window_size 홀수만 가능합니다, default = 5
		:type window_Size: int
		:param min_count: 이 수 아래로 등장하는 단어는 무시합니다. default = 5
		:type min_count: int
		:param threads: 사용할 쓰레드의 개수, default = 8
		:type threads: int
		:param iter: 한 코퍼스를 학습하는 횟수, default = 1
		:type iter: int
		:raises: NotImplementedError
		"""
		raise NotImplementedError()

	@abstractmethod
	def model_load(self, path, file_type, encoding, errors):
		"""
		train으로 저장하거나 외부에서 받은 word embedding 모델을 불러옵니다.
				
		[description]
		:param path: 불러올 모델의 경로
		:type path: str
		:param file_type: 불러올 모델의 파일 타입입니다. 't'=txt, 'b'=binary
		:type file_type: char
		:param encoding: 불러올 모델의 파일 인코딩입니다. ex)"cp949", "utf-8", "euc-kr", ...
		:type encoding: str
		:param errors: 불러올 모델의 파일 에러 핸들링을 결정합니다.
		:type errors: str
		:raises: NotImplementedError
		"""
		raise NotImplementedError()
		
	@abstractmethod
	def get_vocab(self):
		"""
		모델의 단어 사전을 반환합니다.
		
		[description]
		:raises: NotImplementedError
		"""
		raise NotImplementedError()
		
	@abstractmethod
	def get_vector(self, input, unk):
		"""
		단어를 받고 해당 단어의 워드 임베딩을 반환합니다.
		unk매개변수에 값을 주면, 들어온 input이 사전에 없을경우 unk를 대신 반환합니다.
		[description]
		:param input: 워드 임베딩으로 바꿀 단어
		:type input: str
		:param unk: unknown word를 뜻하는 메타문자
		:type unk: str
		:raises: NotImplementedError
		"""
		raise NotImplementedError()

	@abstractmethod
	def get_all_vector(self):
		"""
		임베딩 리스트를 반환합니다. 
		
		[description]
		:raises: NotImplementedError
		"""
		raise NotImplementedError()
