# -*- coding: utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: korean converter
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
#         Hyunyoung Lee <hyun02.engineer@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
"""kconv - 한국어 인코딩 변환도구

kconv 는 국민대학교 강승식 교수의 한국어 인코딩 변환 도구 입니다.
파일이나 스트링에 대한 인코딩 변환을 도와주는 도구들이 있습니다.
EUC-KR, UTF-8, UTF-16-LE, UTF-16-BE 간의 인코딩 변환을 지원합니다.

Example:
    >>> from konlp.misc import kconv
    >>> sample_txt = "안녕하세요. 국민대학교 자연어처리 연구실입니다."
    >>> encoded_txt = kconv.convert(sample_txt, 'EUC_KR', 'UTF_8')
    >>> encoded_txt
    b'\xec\x95\x88\xeb\x85\x95\xed\x95\x98\xec\x84\xb8\xec\x9a\x94. \xea\xb5\xad\xeb\xaf\xbc\xeb\x8c\x80\xed\x95\x99\
    \xea\xb5\x90 \xec\x9e\x90\xec\x97\xb0\xec\x96\xb4\xec\xb2\x98\xeb\xa6\xac \xec\x97\xb0\xea\xb5\xac\xec\x8b\xa4\xec\
    \x9e\x85\xeb\x8b\x88\xeb\x8b\xa4.'
    >>> file_dir = 'input.txt'
    >>> kconv.scan(file_dir)
    >>> kconv.convert_file(file_dir, 'output.txt', 'UTF_8', 'UTF_16_LE')

"""
import os

from .lib.kconv_wrapper import convert as _convert
from .lib.kconv_wrapper import convert_file as _convert_file
from .lib.kconv_wrapper import scan as _scan
from .lib.kconv_wrapper import synopsis as _synopsis


def _cvt_enc_name(enc):
    """인코딩 이름 변환 함수

    사용자가 정의한 인코딩 이름을 kconv 인코딩 이름 규칙에 맡게 변환하는 함수.
    EUC_KR, CP949, UTF_8, UTF_8_BOM, UTF_16_LE, UTF_16_BE 이 존재.

    Args:
        enc (str): 사용자가 정의한 인코딩 이름

    Returns:
        str: kconv 인코딩 이름

    Raises:
        ValueError: 정의되지 않은 인코딩 이름이 들어올 경우 발생

    """
    class Encoding:
        """인코딩 이름 클래스"""

        CP949 = 'CP949'
        EUC_KR = 'EUC_KR'
        UTF_8 = 'UTF_8'
        UTF_8_BOM = 'UTF_8_BOM'
        UTF_16_LE = 'UTF_16_LE'
        UTF_16_BE = 'UTF_16_BE'

    enc = enc.lower().replace('_', '').replace('-', '')

    if enc == 'cp949':
        return Encoding.CP949
    elif enc == 'euckr':
        return Encoding.EUC_KR
    elif enc == 'utf8':
        return Encoding.UTF_8
    elif enc == 'utf8bom':
        return Encoding.UTF_8_BOM
    elif enc == 'utf16le':
        return Encoding.UTF_16_LE
    elif enc == 'utf16be':
        return Encoding.UTF_16_BE
    else:
        raise ValueError('Unknown encoding type : {}'.format(enc))

def synopsis():
    """kconv 사용 설명 함수"""

    _synopsis()

def convert(string, in_enc, out_enc):
    """스트링 인코딩 변환 함수

    주어진 스트링과 인코딩 변환 규칙을 바탕으로 인코딩 작업을 수행합니다.
    스트링은 str, bytes 타입이여야 하고, 반환값은 항상 bytes 타입입니다.
    입력 스트링의 타입이 str 일 경우, 입력 인코딩을 자동으로 `EUC_KR`로 인식됩니다.

    Args:
        string (str): 혹은 bytes 타입도 가능. 인코딩 변환할 스트링.
        in_enc (str): string의 현재 인코딩 타입.
        out_enc (str): 변환할 인코딩 타입.

    Returns:
        bytes: 인코딩 변환된 bytes string

    """
    if not isinstance(string, str) and not isinstance(string, bytes):
        raise TypeError('string type must be string or bytes')

    in_enc = _cvt_enc_name(in_enc)
    out_enc = _cvt_enc_name(out_enc)

    return _convert(string, in_enc, out_enc)

def convert_file(infile_dir, outfile_dir, in_enc, out_enc):
    """파일 인코딩 변환 함수

    주어진 파일 경로와 인코딩 변환 규칙을 바탕으로 인코딩 작업을 수행합니다.
    인코딩 변환된 파일은 저장 경로에 항상 덮어씁니다.

    Args:
        infile_dir (str): 변환할 파일 경로
        outfile_dir (str): 변환된 파일의 경로
        in_enc (str): 현재 파일의 인코딩 타입
        out_enc (str): 변환된 파일의 인코딩 타입

    """
    if not os.path.exists(infile_dir):
        raise FileNotFoundError('Can not find infile in the path : {}'.format(infile_dir))

    in_enc = _cvt_enc_name(in_enc)
    out_enc = _cvt_enc_name(out_enc)

    _convert_file(infile_dir, outfile_dir, in_enc, out_enc)

def scan(file_dir):
    """파일 인코딩 탐지 함수

    주어진 파일 경로에서 파일의 인코딩을 탐지하는 함수입니다.

    Args:
        file_dir (str): 인코딩을 탐지할 파일 경로

    Returns:
        int: 인코딩 타입

    """
    if not os.path.exists(file_dir):
        raise FileNotFoundError('Can not find file in the path : {}'.format(file_dir))

    return _scan(file_dir)
