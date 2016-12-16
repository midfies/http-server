# -*- coding: utf-8 -*-
"""Tests for http-server client and server modules."""

import pytest

HTTP_REQ_TABLE = [
    # passes
    ['GET /path/to/index.html HTTP/1.1', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # passes
    ['GET /to/index.html HTTP/1.1', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # passes
    ['GET index.html HTTP/1.1', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # fails because of PUT
    ['PUT /path/to/index.html HTTP/1.1', 'HTTP/1.1 500 Internal Server Error\r\nThis server only accepts GET requests\r\n\r\n'],
    # fails because of HTTP/1.0
    ['GET /path/to/index.html HTTP/1.0', 'HTTP/1.1 500 Internal Server Error\r\nClient must use HTTP/1.1\r\n\r\n'],
    # fails for not enough arguments
    ['GET /path/to/index.html', "HTTP/1.1 500 Internal Server Error\r\nHTTP Request requires 3 Method, URI, and Protocol.\r\n\r\n"],
    # fails for too many arguments
    ['GET /path/to/index.html HTTP/1.1 Additional', "HTTP/1.1 500 Internal Server Error\r\nUnknown arguements passed with request.\r\n\r\n"],
]


@pytest.mark.parametrize("message, response", HTTP_REQ_TABLE)
def test_message_less_than_buffer(message, response):
    """Test message is smaller than a buffer."""
    from client import client
    assert client(message) == response


def test_server_error():
    """Test server error."""
    from server import response_error
    assert response_error("adfafa") == '''HTTP/1.1 500 Internal Server Error\r\nUnknown arguements passed with request.\r\n\r\n'''
