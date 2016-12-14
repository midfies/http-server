# -*- coding: utf-8 -*-
"""Tests for http-server client and server modules."""

import pytest


MSG_TABLE = [
    ('Msg'),
    ('MsgEIGHT'),
    ('Msg long is a really long buffer'),
    ('MsgEIGHTMsgEIGHTMsgEIGHT'),

]


@pytest.mark.parametrize("message", MSG_TABLE)
def test_message_less_than_buffer(message):
    """Test message is smaller than a buffer."""
    from client import client
    assert client(message) == message
