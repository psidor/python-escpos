#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""tests for the magic encode module

:author: `Patrick Kanzler <patrick.kanzler@fablab.fau.de>`_
:organization: `python-escpos <https://github.com/python-escpos>`_
:copyright: Copyright (c) 2016 `python-escpos <https://github.com/python-escpos>`_
:license: GNU GPL v3
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from nose.tools import raises, assert_raises
from hypothesis import given, example
import hypothesis.strategies as st
from escpos.magicencode import MagicEncode
from escpos.exceptions import CharCodeError, Error
from escpos.constants import CHARCODE

@raises(CharCodeError)
def test_magic_encode_unkown_char_constant_as_startenc():
    """tests whether MagicEncode raises the proper Exception when an unknown charcode-name is passed as startencoding"""
    MagicEncode(startencoding="something")

@raises(CharCodeError)
def test_magic_encode_unkown_char_constant_as_defaultenc():
    """tests whether MagicEncode raises the proper Exception when an unknown charcode-name is passed as defaultenc."""
    MagicEncode(defaultencoding="something")

def test_magic_encode_wo_arguments():
    """tests whether MagicEncode works in the standard configuration"""
    MagicEncode()

@raises(Error)
def test_magic_encode_w_non_binary_defaultsymbol():
    """tests whether MagicEncode catches non-binary defaultsymbols"""
    MagicEncode(defaultsymbol="non-binary")

@given(symbol=st.binary())
def test_magic_encode_w_binary_defaultsymbol(symbol):
    """tests whether MagicEncode works with any binary symbol"""
    MagicEncode(defaultsymbol=symbol)

@given(st.text())
@example("カタカナ")
@example("あいうえお")
@example("ﾊﾝｶｸｶﾀｶﾅ")
def test_magic_encode_encode_text_unicode_string(text):
    """tests whether MagicEncode can accept a unicode string"""
    me = MagicEncode()
    me.encode_text(text)

@given(char=st.characters())
def test_magic_encode_encode_char(char):
    """tests the encode_char-method of MagicEncode"""
    me = MagicEncode()
    me.encode_char(char)

@raises(Error)
@given(char=st.binary())
def test_magic_encode_encode_char_binary(char):
    """tests the encode_char-method of MagicEncode with binary input"""
    me = MagicEncode()
    me.encode_char(char)


def test_magic_encode_string_with_katakana_and_hiragana():
    """tests the encode_string-method with katakana and hiragana"""
    me = MagicEncode()
    me.encode_str("カタカナ")
    me.encode_str("あいうえお")

@raises(CharCodeError)
def test_magic_encode_codepage_sequence_unknown_key():
    """tests whether MagicEncode.codepage_sequence raises the proper Exception with unknown charcode-names"""
    MagicEncode.codepage_sequence("something")

@raises(CharCodeError)
def test_magic_encode_codepage_name_unknown_key():
    """tests whether MagicEncode.codepage_name raises the proper Exception with unknown charcode-names"""
    MagicEncode.codepage_name("something")

def test_magic_encode_constants_getter():
    """tests whether the constants are properly fetched"""
    for key in CHARCODE:
        name = CHARCODE[key][1]
        if name == '':
            assert_raises(CharCodeError, MagicEncode.codepage_name, key)
        else:
            assert name == MagicEncode.codepage_name(key)
        assert MagicEncode.codepage_sequence(key) == CHARCODE[key][0]

def test_magic_encode_force_encoding():
    """test whether force_encoding works as expected"""
    me = MagicEncode()
    assert me.force_encoding is False
    me.set_encoding(encoding='KATAKANA', force_encoding=True)
    assert me.encoding == 'KATAKANA'
    assert me.force_encoding is True