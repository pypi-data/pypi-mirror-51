# -*- coding: utf-8 -*-

import string

from bceauth.utils import uri_encode, uri_encode_except_slash


def test_uri_encode():
    assert string.digits == uri_encode(string.digits)
    assert string.ascii_letters == uri_encode(string.ascii_letters)
    assert '%21%22%23%24%25%26%27%28%29%2A%2B%2C-.%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~' == uri_encode(  # noqa
        string.punctuation)
    assert '%20%09%0A%0D%0B%0C' == uri_encode(string.whitespace)


def test_uri_encode_except_slash():
    assert string.digits == uri_encode_except_slash(string.digits)
    assert string.ascii_letters == uri_encode_except_slash(
        string.ascii_letters)
    assert '%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~' == uri_encode_except_slash(  # noqa
        string.punctuation)
    assert '%20%09%0A%0D%0B%0C' == uri_encode_except_slash(string.whitespace)
