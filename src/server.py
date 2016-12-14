# -*- coding: utf-8 -*-
"""Server.py for python echo server."""

import socket
import sys


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    while True:
        print("Waiting for connection...")
        try:
            conn, addr = server.accept()
            if conn:
                logged_message = ''
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    logged_message += part.decode('utf8')
                    if len(part) < buffer_length:
                        break
            if logged_message[-3:] == 'EOF':
                logged_message = logged_message[:-3]
            print(logged_message)
            conn.sendall(response_ok().encode('utf8'))
            print("Connection Received Succesfully")
        except KeyboardInterrupt:
            break
        except(RuntimeError, SyntaxError, UnicodeError):
            conn.sendall(response_error().encode('utf8'))
            print("DANGER INTERNAL SERVER ERROR!! OVERLOAD OVERLOAD")
        finally:
            if conn:
                conn.close()
    server.close()
    print('Thanks for visiting!')
    sys.exit()


def response_ok():
    """Send a 200 response."""
    return """
    HTTP/1.1 200 OK\r\n
    Content-Type: text/plain \r\n
    \r\n
    Thanks for connecting, friend."""


def response_error():
    """Send a 500 Server Error."""
    return """
    HTTP/1.1 500 Internal Server Error\r\n
    Content-Type: text/plain\r\n
    \r\n
    You did a bad, bad thing."""


if __name__ == '__main__':
    """Run server if run from command line"""
    server()
