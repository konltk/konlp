# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: Autospacing of klt
#
# Author: Younghun Cho <cyh905@gmail.com>
#         Hyunyoung Lee <hyun02.engineer.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""Klt Tokenizer"""

# for the load dic files
import konlp
from konlp.tokenize.klt.lib import klt_asp as _klt_asp

def klt_asp(text, dic_path="", split=True):
    """
    국민대학교 강승식 교수님의 자동 띄어쓰기 기능입니다.
    한글 문장이 주어지면 자동 띄어쓰기를 진행 후,
    공백(white-space) 기준으로 tokenize를 합니다.

    Args:
        string(str): 띄어쓰기를 할 문장
        dic_path(str): 사전 폴더의 위치
        split(bool): 결과를 split할지 결정 하는 변수
    Returns:
        list: tokenize된 list
        string: 만약 split이 `Flase`이면 한 문장

    Example:
        >>> from konlp.tokenize import klt_asp
        >>> klt_asp(text="국민대학교자연어처리연구실")
        ['국민대학교', '자연어처리', '연구실']
        >>> klt_asp(text="국민대학교자연어처리연구실", split=False)
        '국민대학교 자연어처리 연구실'
        >>> klt_asp(text="국민대학교자연어처리연구실", split=True)
        ['국민대학교', '자연어처리', '연구실']
    """
    def _dic_init(dic_path):
        """사전을 초기화하는 함수입니다.
        만약 초기화가 안된다면 사전을 다시 load를 하여서 초기화를 해야합니다.
        사전이 초기화가 안되어 있다면 자동 띄어쓰기가 작동이 안됩니다.

        Args:
            dic_path(str): 사전 위치
        """
        result_init = _klt_asp.dic_init(dic_path) # pylint: disable=I1101
        if result_init == 1:
            print("Can't load dictionary file")
            print("You have to load dictionary file use 'dic_init'")
            print("path: "+ dic_path)

    if dic_path == "":
        dic_path = konlp.__path__[0] + "/tokenize/klt/data/dic/"

    _dic_init(dic_path)

    return _klt_asp.asp(text).split(" ")  if split else _klt_asp.asp(text) # pylint: disable=I1101
