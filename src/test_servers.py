# -*- coding: utf-8 -*-
"""Tests for http-server client and server modules."""

import pytest


MSG_TABLE = [
    ('Msg'),
    ('MsgEIGHT'),
    ('Msg long is a really long buffer'),
    ('MsgEIGHTMsgEIGHTMsgEIGHT'),
    ('§¡¢§'),
]


@pytest.mark.parametrize("message", MSG_TABLE)
def test_message(message):
    """Test message based on various lengths."""
    from client import client
    assert client(message) == """
    HTTP/1.1 200 OK\r\n
    Content-Type: text/plain \r\n
    \r\n
    Thanks for connecting, friend."""


def test_server_error():
    """Test server error."""
    from server import response_error
    assert response_error() == """
    HTTP/1.1 500 Internal Server Error\r\n
    Content-Type: text/plain\r\n
    \r\n
    You did a bad, bad thing."""
