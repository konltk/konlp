# -*- coding:utf8 -*-
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: korean converter
#
# Author: GyuHyeon Nam <ngh3053@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================
import os
import pytest

from konlp.misc import kconv


TEMP_DIR = os.path.join(os.path.dirname(__file__), 'files/temp.txt')

def file_diff(dir1, dir2):
    with open(dir1, 'rb') as f1, open(dir2, 'rb') as f2:
        assert f1.read() == f2.read()

@pytest.fixture
def string():
    return "안녕하세요. 국민대학교 자연어처리 연구실입니다."

@pytest.fixture
def euckr():
    return b'\xbe\xc8\xb3\xe7\xc7\xcf\xbc\xbc\xbf\xe4. \xb1\xb9\xb9\xce\xb4\xeb\xc7\xd0\xb1\xb3 \xc0\xda\xbf\xac\xbe\xee\xc3\xb3\xb8\xae \xbf\xac\xb1\xb8\xbd\xc7\xc0\xd4\xb4\xcf\xb4\xd9.'

@pytest.fixture
def utf8():
    return b'\xec\x95\x88\xeb\x85\x95\xed\x95\x98\xec\x84\xb8\xec\x9a\x94. \xea\xb5\xad\xeb\xaf\xbc\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90 \xec\x9e\x90\xec\x97\xb0\xec\x96\xb4\xec\xb2\x98\xeb\xa6\xac \xec\x97\xb0\xea\xb5\xac\xec\x8b\xa4\xec\x9e\x85\xeb\x8b\x88\xeb\x8b\xa4.'

@pytest.fixture
def utf16le():
    return b'H\xc5U\xb1X\xd58\xc1\x94\xc6.\x00 \x00m\xad\xfc\xbb\x00\xb3Y\xd5P\xad \x00\x90\xc7\xf0\xc5\xb4\xc5\x98\xcc\xac\xb9 \x00\xf0\xc5l\xad\xe4\xc2\x85\xc7\xc8\xb2\xe4\xb2.\x00'

@pytest.fixture
def utf16be():
    return b'\xc5H\xb1U\xd5X\xc18\xc6\x94\x00.\x00 \xadm\xbb\xfc\xb3\x00\xd5Y\xadP\x00 \xc7\x90\xc5\xf0\xc5\xb4\xcc\x98\xb9\xac\x00 \xc5\xf0\xadl\xc2\xe4\xc7\x85\xb2\xc8\xb2\xe4\x00.'

@pytest.fixture
def euckr_dir():
    return os.path.join(os.path.dirname(__file__), 'files/euckr.txt')

@pytest.fixture
def utf8_dir():
    return os.path.join(os.path.dirname(__file__), 'files/utf8.txt')

@pytest.fixture
def utf16le_dir():
    return os.path.join(os.path.dirname(__file__), 'files/utf16le.txt')

@pytest.fixture
def utf16be_dir():
    return os.path.join(os.path.dirname(__file__), 'files/utf16be.txt')


def test_str_euckr(string, euckr):
    assert kconv.convert(string, "euckr", "euckr") == euckr

def test_str_utf8(string, utf8):
    assert kconv.convert(string, "euckr", "utf8") == utf8

def test_str_utf16le(string, utf16le):
    assert kconv.convert(string, "euckr", "utf16le") == utf16le

def test_str_utf16be(string, utf16be):
    assert kconv.convert(string, "euckr", "utf16be") == utf16be

def test_euckr_utf8(euckr, utf8):
    assert kconv.convert(euckr, "euckr", "utf8") == utf8

def test_euckr_utf16le(euckr, utf16le):
    assert kconv.convert(euckr, "euckr", "utf16le") == utf16le

def test_euckr_utf16be(euckr, utf16be):
    assert kconv.convert(euckr, "euckr", "utf16be") == utf16be

def test_utf8_euckr(utf8, euckr):
    assert kconv.convert(utf8, "utf8", "euckr") == euckr

def test_utf8_utf16le(utf8, utf16le):
    assert kconv.convert(utf8, "utf8", "utf16le") == utf16le

def test_utf8_utf16be(utf8, utf16be):
    assert kconv.convert(utf8, "utf8", "utf16be") == utf16be

def test_utf16le_euckr(utf16le, euckr):
    assert kconv.convert(utf16le, "utf16le", "euckr") == euckr

def test_utf16le_utf8(utf16le, utf8):
    assert kconv.convert(utf16le, "utf16le", "utf8") == utf8

def test_utf16le_utf16be(utf16le, utf16be):
    assert kconv.convert(utf16le, "utf16le", "utf16be") == utf16be

def test_utf16be_euckr(utf16be, euckr):
    assert kconv.convert(utf16be, "utf16be", "euckr") == euckr

def test_utf16be_utf8(utf16be, utf8):
    assert kconv.convert(utf16be, "utf16be", "utf8") == utf8

def test_utf16be_utf16le(utf16be, utf16le):
    assert kconv.convert(utf16be, "utf16be", "utf16le") == utf16le


def test_file_euckr_utf8(euckr_dir, utf8_dir):
    kconv.convert_file(euckr_dir, TEMP_DIR, "euckr", "utf8bom")
    file_diff(TEMP_DIR, utf8_dir)

def test_file_euckr_utf16le(euckr_dir, utf16le_dir):
    kconv.convert_file(euckr_dir, TEMP_DIR, "euckr", "utf16le")
    file_diff(TEMP_DIR, utf16le_dir)

def test_file_euckr_utf16be(euckr_dir, utf16be_dir):
    kconv.convert_file(euckr_dir, TEMP_DIR, "euckr", "utf16be")
    file_diff(TEMP_DIR, utf16be_dir)

def test_file_utf8_euckr(utf8_dir, euckr_dir):
    kconv.convert_file(utf8_dir, TEMP_DIR, "utf8", "euckr")
    file_diff(TEMP_DIR, euckr_dir)

def test_file_utf8_utf16le(utf8_dir, utf16le_dir):
    kconv.convert_file(utf8_dir, TEMP_DIR, "utf8", "utf16le")
    file_diff(TEMP_DIR, utf16le_dir)

def test_file_utf8_utf16be(utf8_dir, utf16be_dir):
    kconv.convert_file(utf8_dir, TEMP_DIR, "utf8", "utf16be")
    file_diff(TEMP_DIR, utf16be_dir)

def test_file_utf16be_euckr(utf16be_dir, euckr_dir):
    kconv.convert_file(utf16be_dir, TEMP_DIR, "utf16be", "euckr")
    file_diff(TEMP_DIR, euckr_dir)

def test_file_utf16be_utf8(utf16be_dir, utf8_dir):
    kconv.convert_file(utf16be_dir, TEMP_DIR, "utf16be", "utf8bom")
    file_diff(TEMP_DIR, utf8_dir)

def test_file_utf16be_utf16le(utf16be_dir, utf16le_dir):
    kconv.convert_file(utf16be_dir, TEMP_DIR, "utf16be", "utf16le")
    file_diff(TEMP_DIR, utf16le_dir)

def test_file_utf16le_euckr(utf16le_dir, euckr_dir):
    kconv.convert_file(utf16le_dir, TEMP_DIR, "utf16le", "euckr")
    file_diff(TEMP_DIR, euckr_dir)

def test_file_utf16le_utf8(utf16le_dir, utf8_dir):
    kconv.convert_file(utf16le_dir, TEMP_DIR, "utf16le", "utf8bom")
    file_diff(TEMP_DIR, utf8_dir)

def test_file_utf16le_utf16be(utf16le_dir, utf16be_dir):
    kconv.convert_file(utf16le_dir, TEMP_DIR, "utf16le", "utf16be")
    file_diff(TEMP_DIR, utf16be_dir)
