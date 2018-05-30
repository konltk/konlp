# -*- coding:utf8 -*-
# Korean Word Embedding : 한국어 단어, 어절 임베딩 학습기 및 사용 툴
#
# Copyright (C) 2017 - 0000 KoNLTK project 
# Author: GeonYeong Kim <uhi7074@gmail.com>
#         
# URL: <http://www.konltk.org>
# For license information, see LICENSE.TXT
"""
한국어 단어, 어절 임베딩

한국어 단어, 어절 임베딩입니다.

Example: 
    >>> from konlp.embedding import KnuWord2Vec
    >>> test = KnuWord2Vec()
    >>> test.train("007.txt", "temp.vocab", "emb.bin", "b")
        Warning: temp.vocab is already exist.
        Warning: emb.bin is already exist.
        Vocab size: 483082
        Words in train file: 2786559
        Vocab size: 61057
        Words in train file: 2202126
        Starting training using file 007.txt
        # cur_iter=1, iter=1
        LR:0.009082 Prog:72.76% Words/s:132.3k Acc:83.2% ETime:0.0h max:1.54 std:0.021 ()
    >>> test.model_load("emb.bin", "b", "utf-8")
    >>> test.get_vector("자신의", unk="UNK")
        [0.24138367176055908, -0.19853226840496063, ...]
    >>> test.get_vector("clearly not in", unk="UNK")
        [0.5665938258171082, -0.5307669043540955, ...]
    >>> test.get_vector("UNK")
        [0.5665938258171082, -0.5307669043540955, ...]

"""
#from __future__ import unicode_literals
import konlp
from konlp.embedding.api import abstract_embedding_model
from io import open
from array import array
import ctypes
import os
import sys

class KnuWord2Vec(abstract_embedding_model):
    """
    강원대 이창기 교수님의 word2vec입니다.
    """
    
    def __init__(self):
        self.encoding = "utf-8"
        self.embedding_list = []
        self.word2idx = {}
        self.so_path = {
            "my_word2vec": konlp.__path__[0] + "/embedding/knu_word2vec/lib/my_word2vec.so",
            "my_word2vocab": konlp.__path__[0] + "/embedding/knu_word2vec/lib/my_word2vocab.so"
        }

    def train(self, input, vocab, output, save_type, size=100, negative_sampling=5, lr=0.025, sample=0.00001, window_size=5, min_count=5, threads=8, iter=1):
        """
        문서를 입력받아 임베딩을 학습하는 메소드입니다.
        
        Args:
            input(string): 학습할 코퍼스 위치
            vocab(string): 코퍼스에 등장하는 단어들을 저장할 위치
            output(string): 학습한 모델을 저장할 경로
            save_type(char): ('t' or 'b'), 모델을 어떤 방식으로 저장할지 결정, w=txt, b=binary
            size(int): 학습할 벡터의 사이즈, default = 100
            negative_sampling(int): negative_sampling, default = 5 (0=ns를 사용하지 않음)
            lr(float): learning rate, default = 0.025
            sample(float): 높은 빈도수의 단어들을 학습에서 랜덤하게 제외합니다., default = 0.00001
            window_size(int): window_size 홀수만 가능합니다, default = 5
            min_count(int): 이 수 아래로 등장하는 단어는 무시합니다. default = 5
            threads(int): 사용할 쓰레드의 개수, default = 8
            iter(int): 한 코퍼스를 학습하는 횟수, default = 1
        """
        
        assert os.path.isfile(input), "Wrong input. it is not file."
        assert save_type in ["b", "t"] , "Wrong save type. use 'b' or 't'."
        if os.path.isfile(vocab): print("Warning: %s is already exist."%vocab)
        if os.path.isfile(output): print("Warning: %s is already exist."%output)
        
        
        text2vocab_args = "-train %s -save-vocab %s"%(input, vocab)
        text2vector_args = "-train %s -read-vocab %s -output %s -binary %s -size %s -negative %s -alpha %s -sample %s -window %s -min-count %s -threads %s -iter %s"%(input, vocab, output, "1" if save_type=="b" else "0", str(size), str(negative_sampling), str(lr), str(sample), str(window_size), str(min_count), str(threads), str(iter))
        
        def run_c_so(prog_name, argv):
            argv = (prog_name+ " " + argv).split() 
            c_program = ctypes.CDLL(self.so_path[prog_name]) # so 로딩
            LP_c_char = ctypes.POINTER(ctypes.c_char) # *char
            LP_LP_c_char = ctypes.POINTER(LP_c_char) # **char
            c_program.main.argtypes = (ctypes.c_int, LP_LP_c_char) # main 함수 인자 세팅
            argc = len(argv) # argc 부분
            argv_v = (LP_c_char * (argc+1))() 
            for i, arg in enumerate(argv) : # cstring용에 맞춰 변환
                enc_arg = arg.encode('utf-8')
                argv_v[i] = ctypes.create_string_buffer(enc_arg)
            
            c_program.main(argc, argv_v) # 실행
        
        run_c_so("my_word2vocab", text2vocab_args)
        run_c_so("my_word2vec", text2vector_args)
        print()

        
    def model_load(self, path, file_type, encoding, errors="ignore"):
        """
        저장된 모델을 불러오는 메소드입니다.
        불러올 파일의 형식(텍스트"t", 바이너리"b")를 지정할 수 있으며
        파일의 인코딩 또한 지정할 수 있습니다. 인코딩을 무시할 경우 그냥 open합니다.
        
        Args:
            path(str): 색인어 추출한 문장
            file_type(char): "t" or "b", 임베딩 모델의 파일 형식
            encoding(str): 파일의 인코딩입니다. 
            errors(str): 키워드 매개변수로 파일 입출력의 에러 핸들링을 결정합니다. 기본으로 ignore입니다.
        """    
        assert file_type in ["t", "b"], "wrong file_type, use only 't' and 'b'."

        self.embedding_list = []
        self.word2idx = {}
        self.encoding = encoding
                    
        if file_type == 't':
            file_obj = open(path, file_type+"r", encoding=encoding, errors=errors)
            
            is_first_line = True
            cnt = 0
            for line in file_obj:
                line_split = line.strip().replace("\n", "").replace("\r", "").split(" ")
                
                if is_first_line:
                    is_first_line = False
                    vocab_size, layer1_size = int(line_split[0]), int(line_split[1])
                    continue
                
                word = line_split[0]
                _emb = list(map(lambda x: float(x), line_split[1:]))
                assert len(_emb) == layer1_size, "wrong embedding size, maybe file damaged."
                self.word2idx[word] = cnt
                self.embedding_list.append(_emb)
                cnt += 1
                
        elif file_type == 'b':
            file_obj = open(path, file_type+"r")
                
            cnt = 0
            header = file_obj.readline().split()
            vocab_size, layer1_size = int(header[0]), int(header[1])
            binary_len = 4 * layer1_size
            for line in range(vocab_size):
                word = b""
                while True:
                    ch = file_obj.read(1)
                    if ch == b' ':
                        word = word.decode(encoding, errors=errors)
                        break
                    if ch != '\n':
                        word += ch
                temp_float_array = array("f")
                self.word2idx[word.replace("\n", "")] = cnt
                temp_float_array.fromstring(file_obj.read(binary_len))
                self.embedding_list.append(temp_float_array.tolist())
                cnt += 1
                
        else:
            print("this line never run.")
            
        file_obj.close()
    
    def get_vocab(self):
        """
        불러온 모델의 사전을 반환합니다.
        
        Returns:
            dict(str->int): word2idx, 임베딩 룩업 테이블과 1:1매칭되는 단어 사전을 반환합니다.
        """
        return self.word2idx
    
    def get_vector(self, input, unk=""):
        """
        단어의 임베딩을 반환합니다.
        
        unk 키워드 매개변수에 미리 설정한 unknown word를 나타내는 메타 단어를 넣으실 경우 
        input이 사전에 없다면, unk를 대신 반환합니다. 디폴트 값은 없으며, knu_word2vec의 사전에는 UNK로 이미 들어가 있습니다.
        
        Args:
            input(str): 워드 임베딩으로 바꿀 단어
            unk(str): unknown word를 뜻하는 메타문자
        Returns:
            list(float): 실수 벡터 형태의 워드임베딩 
        """
        assert (unk is not "") or (input in self.word2idx), input+" word not in vocab"
        
        
        if input in self.word2idx:
            return self.embedding_list[self.word2idx[input]]            
        else:
            return self.embedding_list[self.word2idx[unk]]
        
    def get_all_vector(self):
        """
        임베딩 리스트를 반환합니다.
        
        Returns:
            list(list(float)): 워드 임베딩 룩업 테이블
        """
        return self.embedding_list
        