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
"""embedding interface"""

@add_metaclass(ABCMeta)
class abstract_embedding_model:
    """
    한국어 임베딩 모델 인터페이스
    """
    
    @abstractmethod
    def train(self, input, vocab, output, save_type, size=100, negative_sampling=5, lr=0.025, sample=0.00001, window_size=5, min_count=5, threads=8, iter=1):
        """
        문장들을 입력받아 워드 임베딩을 학습합니다.
        
        Args:
            input(str): 학습할 코퍼스 위치
            vocab(str): 코퍼스에 등장하는 단어들을 저장할 위치
            output(str): 학습한 모델을 저장할 경로
            save_type(char): ('t' or 'b'), 모델을 어떤 방식으로 저장할지 결정, t=txt, b=binary
            size(int): 학습할 벡터의 사이즈, default = 100
            negative_sampling(float): negative_sampling, default = 5 (0=ns를 사용하지 않음)
            lr(float): learning rate, default = 0.025
            sample(float): 높은 빈도수의 단어들을 학습에서 랜덤하게 제외합니다., default = 0.00001
            window_size(int): window_size 홀수만 가능합니다, default = 5
            min_count(int): 이 수 아래로 등장하는 단어는 무시합니다. default = 5
            threads(int): 사용할 쓰레드의 개수, default = 8
            iter(int): 한 코퍼스를 학습하는 횟수, default = 1
        Raises: 
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()

    @abstractmethod
    def model_load(self, path, file_type, encoding, errors):
        """
        train으로 저장하거나 외부에서 받은 word embedding 모델을 불러옵니다.
                
        Args:
            path(str): 불러올 모델의 경로
            file_type(str): 불러올 모델의 파일 타입입니다. 't'=txt, 'b'=binary
            encoding(str): 불러올 모델의 파일 인코딩입니다. ex)"cp949", "utf-8", "euc-kr", ...
            errors(str): 불러올 모델의 파일 에러 핸들링을 결정합니다.
        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()
        
    @abstractmethod
    def get_vocab(self):
        """
        모델의 단어 사전을 반환합니다.
        
        Returns:
            dict(str->int): word2idx, 임베딩 룩업 테이블과 1:1매칭되는 단어 사전을 반환합니다.
        raises: 
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()
        
    @abstractmethod
    def get_vector(self, input, unk):
        """
        단어를 받고 해당 단어의 워드 임베딩을 반환합니다.
        unk매개변수에 값을 주면, 들어온 input이 사전에 없을경우 unk를 대신 반환합니다.
        
        Args:
            input(str): 워드 임베딩으로 바꿀 단어
            unk(str): unknown word를 뜻하는 메타문자
        Returns:
            list(float): 실수 벡터 형태의 워드임베딩 
        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_vector(self):
        """
        임베딩 리스트를 반환합니다. 
        
        Returns:
            list(list(float)): 워드 임베딩 룩업 테이블
        Raises:
            NotImplementedError: 이 클래스를 상속한 클래스가 메소드를 구현하지 않았을 경우 발생
        """
        raise NotImplementedError()
