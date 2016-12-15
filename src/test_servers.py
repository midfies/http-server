# -*- coding: utf-8 -*-
"""Tests for http-server client and server modules."""

import pytest


HTTP_REQ_TABLE = [
    # passes
    ['GET /path/to/index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # passes
    ['GET /to/index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # passes
    ['GET index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n', "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."],
    # fails because of PUT
    ['PUT /path/to/index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n', 'HTTP/1.1 500 Internal Server Error\r\nThis server only accepts GET requests\r\n\r\n'],
    # fails because of HTTP/1.0
    ['GET /path/to/index.html HTTP/1.0\r\nHost: www.example.com\r\n\r\n', 'HTTP/1.1 500 Internal Server Error\r\nClient must use HTTP/1.1\r\n\r\n'],
    # fails for not enough arguments
    ['GET /path/to/index.html\r\nHost: www.example.com\r\n\r\n', "HTTP/1.1 500 Internal Server Error\r\nHTTP Request requires 3 Method, URI, and Protocol.\r\n\r\n"],
    # fails for too many argumentss
    ['GET /path/to/index.html HTTP/1.1 Additional\r\nHost: www.example.com\r\n\r\n', "HTTP/1.1 500 Internal Server Error\r\nUnknown arguements passed with request.\r\n\r\n"],
]

URI_TABLE = [
    ['make_time.py', 'Found in root.'],
    ['sample.txt', 'Found in root.'],
    ['a_web_page.html', 'Found in root.'],
    ['images', 'Found in root.'],
    ['images/sample_1.png', 'Found in sub directory'],
    ['images/JPEG_example.jpg', 'Found in sub directory'],
    ['images/Sample_Scene_Balls.jpg', 'Found in sub directory'],
]


@pytest.mark.parametrize("message, response", HTTP_REQ_TABLE)
def test_message_less_than_buffer(message, response):
    """Test message is smaller than a buffer."""
    from client import client
    assert client(message) == response

@pytest.mark.parametrize('file, response', URI_TABLE)
def test_get_directory_info(file, response):
    """Get the files from the root directory."""
    from server import resolve_uri
    assert resolve_uri(file) == response
