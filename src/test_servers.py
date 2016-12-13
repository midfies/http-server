"""Tests for http-server client and server modules."""


def test_message_less_than_buffer():
    """Test message is smaller than a buffer."""
    from client import client
    assert client("Msg") == "Msg"


def test_message_same_as_buffer():
    """Test message is smaller than a buffer."""
    from client import client

    assert client("MsgEIGHT") == "MsgEIGHT"


def test_message_larger_than_buffer():
    """Test message is smaller than a buffer."""
    from client import client
    assert client("Msg long is a really long buffer") == "Msg long is a really long buffer"
